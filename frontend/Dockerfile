FROM node:14.18

RUN mkdir /app
WORKDIR /app

COPY . ./

RUN yarn
RUN yarn build
RUN yarn add express serve-static
CMD node server.js

EXPOSE 7000
