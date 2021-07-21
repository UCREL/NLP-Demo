FROM node:14.17.3-alpine

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs \
      yarn

ARG USER_ID
ARG GROUP_ID

RUN deluser --remove-home node \
  && addgroup -S node -g $GROUP_ID \
  && adduser -S -G node -u $USER_ID node

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

USER node
