// Offline-Speicher für Tagesteller. Bei Änderungen an der App die Versionsnummer erhöhen.
const CACHE = 'tagesteller-v2';
const FILES = ['./', './index.html', './foods.js', './manifest.json',
  './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  // Online-Produktsuche immer frisch aus dem Netz
  if (url.hostname.endsWith('openfoodfacts.org')) return;
  // App-Dateien: zuerst Netz (für Updates), bei fehlender Verbindung aus dem Speicher
  if (url.origin === location.origin) {
    e.respondWith(fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r;
    }).catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
    return;
  }
  // Schriften: aus dem Speicher, sonst Netz
  if (url.hostname.includes('fonts.g')) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return res;
    })));
  }
});
