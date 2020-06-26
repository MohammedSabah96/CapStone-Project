FROM node:13.12.0-alpine
COPY package.json /data/
COPY package-lock.json /data/
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent
ENV PATH /data/node_modules/.bin:$PATH
COPY . /data/app/
WORKDIR /data/app/
CMD ["npm", "start"]