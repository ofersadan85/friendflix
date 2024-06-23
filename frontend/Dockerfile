FROM node:22.3-alpine3.19 as build

WORKDIR /app
COPY package.json /app
COPY package-lock.json /app
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
