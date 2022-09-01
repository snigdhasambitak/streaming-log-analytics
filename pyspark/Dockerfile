FROM ubuntu/apache2

# credits:
# - https://blog.probablyfine.co.uk/2014/05/05/using-docker-with-apache-flume-1.html
# - https://stackoverflow.com/a/44154721
# install java and wget
RUN apt-get update -q
RUN DEBIAN_FRONTEND=noninteractive apt-get install \
  -qy vim wget net-tools default-jre-headless

RUN mkdir /opt/flume
RUN wget -qO- \
  https://dlcdn.apache.org/flume/1.10.1/apache-flume-1.10.1-bin.tar.gz \
  | tar xvzf - -C /opt/flume --strip 1

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH /opt/flume/bin:$PATH
