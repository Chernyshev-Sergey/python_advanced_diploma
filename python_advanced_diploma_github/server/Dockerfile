FROM python:3.12-slim
RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*
RUN mkdir /server
COPY /server /server
RUN pip install --no-cache-dir --upgrade -r server/app_tweets/requirements.txt
WORKDIR /server/app_tweets
ENV PYTHONPATH=/server/app_tweets
ENTRYPOINT ["python", "main.py"]