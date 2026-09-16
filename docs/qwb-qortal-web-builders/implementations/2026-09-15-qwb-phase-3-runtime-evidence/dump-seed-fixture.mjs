/**
 * Writes the shipped seed bundle as exactly-what-a-QDN-read-would-return JSON,
 * which is the fixture the Phase 3 browser harness serves from its fake node.
 *
 * Usage (from the app repository):
 *   npx vite-node /tmp/qwb-p3-dump-seed.mjs > /tmp/qwb-p3-seed.json
 */
import { createSeedSource } from '/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders/src/content/repository.ts';

const loaded = await createSeedSource().load();
if (loaded.status === 'error') throw new Error('the shipped seed content is invalid');
const { site, highlights, services, steps, works, prices, articles } = loaded.bundle;
const entities = [site, ...highlights, ...services, ...steps, ...works, ...prices, ...articles];
const plain = entities.map((entity) => JSON.parse(JSON.stringify(entity)));
process.stdout.write(JSON.stringify(plain, null, 1));
