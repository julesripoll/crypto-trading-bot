#!/bin/bash

docker build -t extract_data .
docker run --rm -v ${PWD}/csv_files/:/app/csv_files extract_data