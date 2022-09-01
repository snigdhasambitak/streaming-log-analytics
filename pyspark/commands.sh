docker build -t httpd-flume-avro-agent .
docker build -f Dockerfile_avrosrc -t ubuntu-avrosrc-kafkasink .
docker build -f Dockerfile_avro -t http-flume-logging .
docker build -f Dockerfile_pyspark -t pyspark .

#docker run -d --rm --net spa-net --name flume_agent -p 10000:4141 -it ubuntu-avrosrc-kafkasink
docker run -d --rm --net streaming-log-analytics_elk --name flume_agent -it ubuntu-avrosrc-kafkasink
docker run -d --rm -e TZ=UTC --net streaming-log-analytics_elk --name apache2_logger -p 8080:80 http-flume-logging

docker run --rm -it --name pyspark --net streaming-log-analytics_elk pyspark
