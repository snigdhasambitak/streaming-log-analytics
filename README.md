# Streaming log analytics

In this integration <b>filebeat</b> will install in all servers where your application is deployed and <b>filebeat</b> will read and ship latest logs changes from these servers to <b>Kafka</b> topic as configured for this application.

<b>Logstash</b> will subscribe log lines from <b>kafka</b> topic and perform parsing on these lines make relevant changes, formatting, exclude and include fields then send this processed data to <b>Elasticsearch</b> Indexes as centralize location from different servers.

<b>Kibana</b> is linked with <b>Elasticsearch</b> indexes which will help to do analysis by search, charts and dashboards .
<br><br>

# Pipeline
![git_imame](https://user-images.githubusercontent.com/50271311/155036578-c1f2517f-cf4b-4eb0-a9fe-4d25d7031e70.png)
<br><br>


# Getting started 
```bash
git clone https://github.com/snigdhasambitak/streaming-log-analytics.git
docker-compose up -d --build
```
<br>