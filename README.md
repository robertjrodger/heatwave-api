## Setting up a development environment

    % conda env create --file environment.yml
    % conda activate heatwave-api
    % pre-commit install
    % pip install -e .'[dev]'
    
## Debugging

Execute the following from the Terminal in your IDE:

    %  VM_API_DEBUG=True python /path/to/src/heatwave_api/__main__.py

## Running the service locally

    % VM_API_KEYS='s3krit' uvicorn --reload heatwave_api:app
    
To verify that the API is up:

    % curl -H 'X-API-KEY: s3krit' 'http://localhost:8000/ping'

## The service

To obtain heatwave records between, eg. 1 January 2010 and 15 November 2017, inclusive:

    % curl -H 'X-API-KEY: s3krit' 'http://localhost:8000/records?from_inclusive=2010-01-01&to_inclusive=2017-11-15'
    
To obtain a copy of the OpenAPI schema:

    % curl -H 'X-API-KEY: s3krit' 'http://localhost:8000/openapi.json'
    
To view the Swagger UI documentation, point your browser to `http://localhost:8000/docs`.
