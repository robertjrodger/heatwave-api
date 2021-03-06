from setuptools import setup, find_packages

test_dependencies = ["pytest==5.4.1", "pytest-cov==2.8.1"]

lint_dependencies = ["flake8==3.7.9"]

setup(
    name="heatwave-api",
    description="Dutch Heatwave Records API",
    version="1.0.0",
    url="https://github.com/robertjrodger/heatwave-api",
    maintainer="Robert Rodger",
    maintainer_email="woodenrabbit@gmail.com",
    packages=find_packages(include=["src"]),
    package_dir={"": "src"},
    package_data={"": ["openapi.yml"]},
    install_requires=[
        "fastapi==0.60.1",
        "pandas==1.0.3",
        "pyarrow==0.17.0",
        "pydantic==1.6.1",
        "pyspark==2.4.5",
        "requests==2.23.0",
        "starlette==0.13.6",
        "uvicorn==0.11.8",
    ],
    extras_require={
        "test": test_dependencies,
        "lint": lint_dependencies,
        "dev": test_dependencies + lint_dependencies,
    },
)
