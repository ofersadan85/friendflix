# The first image we use is used only for building our vite-react app.
# We won't be running the app in this image, so we don't need to expose any ports or volumes.
FROM node:22.3-alpine3.19 as build

# We set the working directory in the container
WORKDIR /app

# We install the required libraries first to leverage Docker's cache
COPY package.json /app
COPY package-lock.json /app
RUN npm install

# After everything is installed, we copy the source code
COPY . .

# This ARG is used to set the VITE_BACKEND_URL environment variable
# It's different from using ENV, as ARG is only available during the build process
ARG VITE_BACKEND_URL=http://www.example.com
# This command will create a .env.production file with the VITE_BACKEND_URL environment variable
RUN sh -c echo "VITE_BACKEND_URL=${VITE_BACKEND_URL}" > .env.production
# This command will build the app (html, css, js, etc.) with the VITE_BACKEND_URL from the .env.production file
RUN npm run build


# The second image is used to serve the built app
# This is the actual container that will run the app
FROM nginx:alpine

# We copy the built app from the first image to the second image
COPY --from=build /app/dist /usr/share/nginx/html

# We don't need to expose any ports, as Nginx will listen on port 80 by default
# We don't need to specify a CMD, as Nginx will start automatically
# We don't need to specify a WORKDIR, as Nginx will serve the files from /usr/share/nginx/html
# We don't need to specify a VOLUME, as we won't be writing any files to the container
# We don't need to specify any environment variables, as Nginx doesn't need any
