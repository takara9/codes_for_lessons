FROM alpine:latest
RUN apk add --no-cache nodejs
ADD ./node_modules /node_modules
ADD ./webapl.js /
CMD node /webapl.js