FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5500

CMD [ "python3", "./log-generator.py", "-n", "100", "-o", "LOG", "-s", "2", "-p", "/usr/share/elasticsearch/logs/" ]