const CACHE_NAME = "offline-cache-v1";
const urlsToCache = [
  "/",
  "/manifest",
  "/icon.png",
 ];

// Instala el SW y guarda en caché los archivos estáticos
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Responde con caché si no hay conexión
self.addEventListener("fetch", (event) => {
  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request).then((response) => response || caches.match("/"))
    )
  );
});