# Chocs Example api
This repository contains example Rest API with usage kodemore libraries: kink, gata and chocs.

It is possible to play around with working api [here](https://chocs-api.herokuapp.com)

Open API Doc is available [here](openapi.yml)

## Running locally
In order to run api locally make sure you have python > 3.7 and poetry available on your machine. 

```shell script
poetry install
poetry shell
python main.py
```

Service should be running on localhost under port `5000`. To change the port simply setup
env variable `$PORT` to desired port.
