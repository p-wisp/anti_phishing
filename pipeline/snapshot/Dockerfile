FROM mcr.microsoft.com/playwright:v1.55.0-noble

WORKDIR /srv

COPY package.json .
RUN npm install --omit=dev

COPY worker.js .

CMD ["node", "worker.js", "https://example.com"]