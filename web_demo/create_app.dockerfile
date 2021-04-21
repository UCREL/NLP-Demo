FROM node:15.14.0-alpine3.10
RUN apk add --no-cache libc6-compat

ARG USER_ID
ARG GROUP_ID

RUN deluser --remove-home node \
  && addgroup -S node -g $GROUP_ID \
  && adduser -S -G node -u $USER_ID node

#RUN mkdir -p /home/node/app && \
#    chown -R npm:npm /home/node/app
USER node