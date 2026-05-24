FROM node:18-alpine
WORKDIR /usr/src/app

ENV NODE_OPTIONS=--openssl-legacy-provider
ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./

EXPOSE 3000
CMD ["npm", "start"]
