#!/bin/bash

docker build -t extract_data .
docker run --rm --network="host" -v $(pwd)/CSV_Files/:/app/CSV_Files extract_data