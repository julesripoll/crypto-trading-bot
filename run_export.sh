#!/bin/bash

echo "docker run --rm -v ${PWD}/ExportData/csv_files/:/app/csv_files extract_data $@"

mkdir -p ExportData/csv_files
docker build -f ExportData/Dockerfile -t extract_data .
docker run --rm -v ${PWD}/ExportData/csv_files/:/app/csv_files extract_data -c 'BTCBUSD' -i '1d'
#cp csv_files/*.csv Data/
# rm -rf csv_files