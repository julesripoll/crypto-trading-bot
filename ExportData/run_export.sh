#!/bin/bash

#echo "docker run --rm -v ${PWD}/ExportData/csv_files/:/app/csv_files extract_data $@"

#mkdir -p csv_files
docker build -t exportdata .
docker run --rm -v ${PWD}/csv_files/:/app/csv_files exportdata -c 'BTCBUSD' -i '15m'
#cp csv_files/*.csv Data/
# rm -rf csv_files