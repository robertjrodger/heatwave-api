## Setting up a development environment

    % conda env create --file environment.yml
    % conda activate heatwave-api
    % pre-commit install
    % pip install -e .'[dev]'

## Running the service locally

    % uvicorn --reload heatwave_api:app
    
To verify that the API is up:

    % curl 'http://localhost:8000/ping'

## The service

To obtain heatwave records between, eg. 1 January 2010 and 15 November 2017, inclusive:

    % curl 'http://localhost:8000/records?from_inclusive=2010-01-01&to_inclusive=2017-11-15'
    
To obtain a copy of the OpenAPI schema:

    % curl 'http://localhost:8000/openapi.json'
    
To view the Swagger UI documentation, point your browser to `http://localhost:8000/docs`.
