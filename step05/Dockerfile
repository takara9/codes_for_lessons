FROM alpine:latest
RUN apk update && apk add bash
ADD ./my_daemon /my_daemon
CMD ["/bin/bash", "/my_daemon"]

