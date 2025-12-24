import { writable } from "svelte/store";
import type { Device } from "$lib/types/device";

export const devices = writable<Device[]>([]);
