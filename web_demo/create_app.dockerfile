FROM node:15.14.0

ARG USER_ID
ARG GROUP_ID

RUN groupmod -g $GROUP_ID node && usermod -u $USER_ID -g $GROUP_ID node

USER node