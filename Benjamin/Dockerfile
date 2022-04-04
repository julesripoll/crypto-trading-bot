# Docker image with PYTHON3 and DEPENDENCES for pyodbc with MS ODBC 17 DRIVER, Debian GNU/Linux 10 (buster)
# BY TADEO RUBIO
# Using the official Python image, Tag 3.8.3-buster
FROM tadeorubio/pyodbc-msodbcsql17

RUN pip3 install pandas
RUN pip3 install pyodbc==4.0.28

WORKDIR /app
COPY extract_data.py extract_data.py
CMD ["python3", "extract_data.py", "-c", "BTCBUSD"]