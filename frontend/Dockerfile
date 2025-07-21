FROM node:20
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
# Dieser Befehl kann je nach Vue-Setup 'serve' oder 'dev' sein. Prüfe deine package.json
CMD ["npm", "run", "dev"]