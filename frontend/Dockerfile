# Frontend Dockerfile
FROM node:14
WORKDIR /frontend
COPY package.json package-lock.json* /frontend/
RUN npm install
COPY . /frontend/
EXPOSE 3000
CMD ["npm", "start"]