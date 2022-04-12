FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

# install FreeTDS and dependencies
RUN apt-get update \
    && apt install python3-pip -y \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y

# populate "ocbcinst.ini" as this is where ODBC driver config sits
RUN echo "[FreeTDS]\n\
    Description = FreeTDS Driver\n\
    Driver = /usr/lib/aarch64-linux-gnu/odbc/libtdsodbc.so\n\
    Setup = /usr/lib/aarch64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

WORKDIR /app

ADD requirements.txt .
ADD main.py .

#Pip command without proxy setting
RUN pip install -r requirements.txt

CMD ["python3","-i","main.py"]