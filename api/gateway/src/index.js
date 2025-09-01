import express from 'express';
import cors from 'cors';
import { createScoreRouter } from './routes/score.js';

/*
 * Gateway server entry point.
 *
 * This server acts as the public HTTP interface for the browser extension.
 * It proxies scoring requests to the inference service and serves a static
 * blocklist for demonstration purposes. By running this server in its own
 * container, we isolate the Node.js runtime from the Python inference
 * service while still allowing them to communicate over the Docker Compose
 * network. The INFERENCE_URL environment variable points to the inference
 * service – in Compose this resolves to http://inference:8000.
 */

const app = express();
app.use(express.json());
// Allow all origins. In production you may want to restrict this.
app.use(cors({ origin: '*' }));

// Determine the inference service URL. If running under Docker Compose this
// defaults to http://inference:8000. When running locally you can override
// this with an environment variable.
const inferenceUrl = process.env.INFERENCE_URL || 'http://inference:8000';

// Health check endpoint used by Docker to verify the service is ready.
app.get('/health', (_req, res) => {
  res.json({ ok: true });
});

// Score API routes. Delegates to a router that proxies requests to the
// inference service.
app.use('/v1/score', createScoreRouter(inferenceUrl));

// Provide a static DNR blocklist. The Chrome extension fetches this to
// populate declarativeNetRequest rules. In a real application this would
// be generated from feeds and updated regularly.
app.get('/v1/lists/block', (_req, res) => {
  res.json([
    {
      id: 1,
      priority: 1,
      action: { type: 'block' },
      condition: { urlFilter: 'malicious.example', resourceTypes: ['main_frame'] }
    }
  ]);
});

// Start the server. Use the PORT environment variable if provided.
const port = parseInt(process.env.PORT, 10) || 8080;
app.listen(port, () => {
  console.log(`Gateway listening on port ${port}`);
});