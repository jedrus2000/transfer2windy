FROM python:3.7

# Set working directory
WORKDIR /usr/src/app

# Update apt-get
# Running separately so that it can be cached
RUN apt-get -y update

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./transfer2windy ./transfer2windy

ENTRYPOINT ["python", "-m", "transfer2windy"]
