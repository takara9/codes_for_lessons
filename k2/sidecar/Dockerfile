FROM ubuntu:16.04
RUN apt-get update && apt-get install -y git vim
COPY ./dev/contents-puller /contents-puller
WORKDIR /
CMD ["/contents-puller"]
