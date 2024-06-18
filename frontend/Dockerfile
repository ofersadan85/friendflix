# Nginx is an extremely popular open-source web server
# We'll use it to just serve the static files created by our frontend build
# ! TODO: This is missing an important first step: building the frontend dist folder
# ! Without it, you must run "npm run build" before building the Docker image!
# ! We'll fix it soon
FROM nginx:alpine

# Copy the static files from the dist folder to the Nginx folder
# By default, Nginx serves files from /usr/share/nginx/html
# We can do many other more advanced configurations, but this is enough for now
COPY dist /usr/share/nginx/html

# We're done! We dont need anything else because:
# We don't need to expose the port (80), as the Nginx image already does that
# We don't need to specify the host (0.0.0.0), as Nginx listens on all interfaces by default
# We don't specify the CMD / ENTRYPOINT, as the Nginx image already does that
