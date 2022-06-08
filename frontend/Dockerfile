FROM node:14.18

ARG BACKEND_URL
ENV BACKEND_URL=$BACKEND_URL

RUN mkdir /app
WORKDIR /app

COPY . ./

RUN yarn
RUN yarn build
RUN yarn add express serve-static
CMD node server.js

EXPOSE 7000
