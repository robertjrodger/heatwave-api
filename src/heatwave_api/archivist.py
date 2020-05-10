from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql import functions as sf


class HeatwaveRecordsArchivist:
    NOT_HEATWAVE_INDICATOR = -1
    HEATWAVE_MIN_TEMPERATURE = 25.0
    TROPICAL_DAY_MIN_TEMPERATURE = 30.0
    HEATWAVE_MIN_DURATION = 5
    HEATWAVE_MIN_NUMBER_TROPICAL_DAYS = 3

    __slots__ = ("data_dir", "spark")

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.spark = self._get_spark_session()

    @staticmethod
    def _get_spark_session() -> SparkSession:
        return (
            SparkSession.builder.appName("heatwave_record_generator")
            .config("spark.sql.execution.arrow.enabled", "true")
            .config("spark.sql.session.timeZone", "UTC")
            .getOrCreate()
        )

    def generate_records(self, output_filepath: Path):
        raw_data_ddf = self.spark.read.text(
            str(self.data_dir / "1.0" / "1.0" / "*" / "*" / "*" / "*.gz")
        )
        daily_max_temperatures_ddf = self._extract_daily_max_temperatures(raw_data_ddf)
        heatwave_records_ddf = self._generate_heatwave_records(
            daily_max_temperatures_ddf
        )
        self._save_heatwave_records(heatwave_records_ddf, output_filepath)

    @staticmethod
    def _extract_daily_max_temperatures(raw_data: DataFrame) -> DataFrame:
        return (
            raw_data.where(~sf.col("value").startswith("#"))
            .withColumn("date", sf.substring(sf.col("value"), 1, 10))
            .withColumn("location", sf.rtrim(sf.substring(sf.col("value"), 22, 20)))
            .withColumn(
                "tx_dryb_10",
                sf.rtrim(sf.substring(sf.col("value"), 310, 20)).cast("float"),
            )
            .where(sf.col("location") == "260_T_a")
            .where(sf.col("tx_dryb_10").isNotNull())
            .groupBy("date")
            .agg(sf.max("tx_dryb_10").alias("max_temperature"))
        )

    def _find_potential_heatwaves(self, ddf):
        previous_temp_window = Window.orderBy("date").rowsBetween(-1, -1)
        upcoming_five_days_window = Window.orderBy("date").rowsBetween(
            Window.currentRow, self.HEATWAVE_MIN_DURATION - 1
        )

        potential_start_dates = (
            ddf.withColumn(
                "previous_max_temperature",
                sf.lag("max_temperature").over(previous_temp_window),
            )
            .withColumn(
                "min_temperature_in_upcoming_five_days",
                sf.min("max_temperature").over(upcoming_five_days_window),
            )
            .where(
                (sf.col("previous_max_temperature") < self.HEATWAVE_MIN_TEMPERATURE)
                & (sf.col("max_temperature") >= self.HEATWAVE_MIN_TEMPERATURE)
                & (
                    sf.col("min_temperature_in_upcoming_five_days")
                    >= self.HEATWAVE_MIN_TEMPERATURE
                )
            )
            .withColumnRenamed("date", "start_date")
            .select("start_date")
            .sort("start_date")
            .toPandas()
        )

        next_temp_window = Window.orderBy("date")
        preceding_five_days_window = Window.orderBy("date").rowsBetween(
            -(self.HEATWAVE_MIN_DURATION - 1), Window.currentRow
        )

        potential_end_dates = (
            ddf.withColumn(
                "next_max_temperature",
                sf.lead("max_temperature").over(next_temp_window),
            )
            .withColumn(
                "min_temperature_in_preceding_five_days",
                sf.min("max_temperature").over(preceding_five_days_window),
            )
            .where(
                (sf.col("next_max_temperature") < self.HEATWAVE_MIN_TEMPERATURE)
                & (sf.col("max_temperature") >= self.HEATWAVE_MIN_TEMPERATURE)
                & (
                    sf.col("min_temperature_in_preceding_five_days")
                    >= self.HEATWAVE_MIN_TEMPERATURE
                )
            )
            .withColumnRenamed("date", "end_date")
            .select("end_date")
            .sort("end_date")
            .toPandas()
        )

        return pd.concat([potential_start_dates, potential_end_dates], axis=1)

    @staticmethod
    def _add_potential_heatwave_ids(ddf, date_ranges_df, id_column):
        for idx, row in date_ranges_df.iterrows():
            ddf = ddf.withColumn(
                id_column,
                sf.when(
                    (sf.col("date") >= row["start_date"])
                    & (sf.col("date") <= row["end_date"]),
                    sf.lit(idx),
                ).otherwise(sf.col(id_column)),
            )
        return ddf

    def _generate_heatwave_records(
        self, daily_max_temperature_data: DataFrame
    ) -> DataFrame:
        potential_heatwave_date_ranges_df = self._find_potential_heatwaves(
            daily_max_temperature_data
        )
        prepped_ddf = daily_max_temperature_data.where(
            sf.col("max_temperature") >= self.HEATWAVE_MIN_TEMPERATURE
        ).withColumn("potential_heatwave_id", sf.lit(self.NOT_HEATWAVE_INDICATOR))
        ided_ddf = self._add_potential_heatwave_ids(
            prepped_ddf, potential_heatwave_date_ranges_df, "potential_heatwave_id"
        )

        return (
            ided_ddf.where(
                sf.col("potential_heatwave_id") != self.NOT_HEATWAVE_INDICATOR
            )
            .groupBy("potential_heatwave_id")
            .agg(
                sf.min("date").alias("from_inclusive"),
                sf.max("date").alias("to_inclusive"),
                sf.count("date").alias("duration"),
                sf.max("max_temperature").alias("max_temperature"),
                sf.sum(
                    sf.when(
                        sf.col("max_temperature") >= self.TROPICAL_DAY_MIN_TEMPERATURE,
                        1,
                    ).otherwise(0)
                ).alias("number_tropical_days"),
            )
            .where(
                sf.col("number_tropical_days") >= self.HEATWAVE_MIN_NUMBER_TROPICAL_DAYS
            )
            .drop("potential_heatwave_id")
        )

    @staticmethod
    def _save_heatwave_records(heatwave_records: DataFrame, filepath: Path):
        (
            heatwave_records.toPandas()
            .sort_values(by="from_inclusive")
            .to_parquet(filepath)
        )
