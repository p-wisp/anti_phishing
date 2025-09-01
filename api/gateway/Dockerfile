FROM node:20-alpine

# Create application directory
WORKDIR /app

# Install production dependencies only
COPY package.json ./
RUN npm install --omit=dev

# Copy the source code
COPY src ./src

# Expose the HTTP port
EXPOSE 8080

# Install curl for healthcheck probes
RUN apk add --no-cache curl

# Configure healthcheck. Docker will call this periodically to determine
# container liveness and readiness. It relies on the /health endpoint of
# the gateway.
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD curl -fsS http://localhost:8080/health || exit 1

# Run the gateway server. NODE_ENV is production by default in alpine.
CMD ["node", "src/index.js"]