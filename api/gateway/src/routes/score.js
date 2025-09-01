import express from 'express';

/*
 * Create a router that forwards scoring requests to the inference service.
 *
 * The gateway uses this router for the `/v1/score` prefix. When a client
 * posts a URL to `/v1/score/url`, this function forwards the request body
 * to the inference service and relays the response back to the client.
 *
 * @param {string} inferenceUrl The base URL of the inference service.
 * @returns {import('express').Router}
 */
export function createScoreRouter(inferenceUrl) {
  const router = express.Router();

  // Forward POST /url to the inference service. Returns whatever the
  // inference service responds with. If the inference service is
  // unreachable, respond with a 502 Bad Gateway.
  router.post('/url', async (req, res) => {
    try {
      const response = await fetch(`${inferenceUrl}/v1/score/url`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(req.body)
      });
      const text = await response.text();
      // Preserve status and content type from the inference service.
      res.status(response.status)
         .type(response.headers.get('content-type') || 'application/json')
         .send(text);
    } catch (err) {
      console.error('Error contacting inference service:', err);
      res.status(502).json({ error: 'inference_unreachable', detail: String(err) });
    }
  });

  return router;
}