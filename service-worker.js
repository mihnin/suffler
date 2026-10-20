/* Суфлёр — service worker: офлайн-кэш приложения.
   Сценарии пользователя здесь не обрабатываются и никуда не отправляются. */
const CACHE = 'suffler-v6';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './manifest.json',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Сеть в приоритете (чтобы обновления приходили сразу), но не дольше 2,5 с;
// без сети или при медленной сети — мгновенно из кэша. Так приложение работает офлайн.
const NET_TIMEOUT = 2500;
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isNav = req.mode === 'navigate';
  const cacheKey = isNav ? './index.html' : req;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const fromCache = () => (isNav
      ? cache.match('./index.html').then((r) => r || cache.match('./'))
      : cache.match(req, { ignoreSearch: true }));

    const network = fetch(req).then((res) => {
      if (res && res.ok && res.type === 'basic') cache.put(cacheKey, res.clone());
      return res;
    });
    const timeout = new Promise((resolve) => setTimeout(resolve, NET_TIMEOUT, null));
    try {
      const res = await Promise.race([network, timeout]);
      if (res) return res;
    } catch (_) { /* нет сети */ }
    const cached = await fromCache();
    if (cached) return cached;
    try { return await network; } catch (_) {
      return new Response('Нет сети и файл не найден в кэше', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }
  })());
});

self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') self.skipWaiting();
});
