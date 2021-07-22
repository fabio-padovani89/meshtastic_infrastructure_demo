FROM node:14-alpine

WORKDIR /frontend-src

COPY . ./

RUN npm install -g sirv-cli
RUN npm install
RUN npm run-script build

EXPOSE 5000

ENV HOST=0.0.0.0

CMD [ "npm", "start" ]
