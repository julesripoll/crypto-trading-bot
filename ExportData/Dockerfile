FROM tadeorubio/pyodbc-msodbcsql17

RUN pip3 install pandas
RUN pip3 install pyodbc==4.0.28

WORKDIR /app
COPY ExportData/extract_data.py extract_data.py

ENTRYPOINT ["python3", "extract_data.py"]