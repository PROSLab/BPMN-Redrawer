FROM node:14.18

ARG FRONTEND_PORT=7000
ARG BACKEND_URL=http://localhost:5000
ENV FRONTEND_PORT=${FRONTEND_PORT}
ENV BACKEND_URL=${BACKEND_URL}

RUN mkdir /app
WORKDIR /app

COPY . ./

RUN yarn
RUN yarn build
RUN yarn add express serve-static
CMD node server.js

EXPOSE ${FRONTEND_PORT}
