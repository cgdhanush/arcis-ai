FROM node:22-alpine

WORKDIR /app
COPY package.json tsconfig.json vite.config.ts index.html /app/
COPY src /app/src
RUN npm install

EXPOSE 5173
CMD ["npm", "run", "dev"]
