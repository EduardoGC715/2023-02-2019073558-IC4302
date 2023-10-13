FROM node:20-alpine3.17

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY components ./components
COPY lib ./lib
COPY pages ./pages
COPY public ./public
COPY styles ./styles
COPY utils ./utils

RUN npm run build

EXPOSE 3000

cmd ["npm", "run", "dev"]

