import { writable } from "svelte/store";

function persistentStore<T>(key: string, initial: T) {
  const store = writable<T>(initial);

  const stored = localStorage.getItem(key);
  if (stored) {
    store.set(JSON.parse(stored));
  }

  store.subscribe((value) => {
    localStorage.setItem(key, JSON.stringify(value));
  });

  return store;
}

export const pageTitle = persistentStore("page-title", "Dashboard");
