## Setting up a development environment

    % conda env create --file environment.yml
    % conda activate heatwave-api
    % pip install -e .'[dev]'

## Running the service locally

    % uvicorn --reload heatwave_api:app
    
To verify that the API is up:

    % curl 'http://localhost:8000/ping'

    
