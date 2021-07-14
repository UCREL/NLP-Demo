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

RUN mkdir /app \
    && chown -R node:node /app
  
USER node
WORKDIR /app

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

COPY --chown=node:node ./nlp_demo/package.json ./nlp_demo/package-lock.json /app/

RUN npm install 

COPY --chown=node:node * /app/

RUN yarn build --profile 