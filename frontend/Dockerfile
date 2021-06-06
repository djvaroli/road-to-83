FROM node:lts-alpine as build-stage

# now we copy over the app files, install dependencies and build our production app
WORKDIR app/
COPY package.json ./
RUN yarn install
COPY . .
RUN yarn build

# set up nginx as our web-server
FROM nginx:stable-alpine as production-build
COPY --from=build-stage /app/dist/ /usr.share/nginx/html
COPY ./scripts/run.sh .
COPY ./.nginx/ .nginx/

# add the bash command which doesn't come with Alpine images
RUN apk update && apk add bash

# change permissions of our script so that we can run it in the container
RUN ["chmod", "+x", "./run.sh"]
CMD ["/bin/bash", "./run.sh"]
