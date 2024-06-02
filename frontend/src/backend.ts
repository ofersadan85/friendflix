import { useLocalStorage } from "usehooks-ts";
import { User } from "./user";

export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL as string;

export type backdropSize = "w300" | "w780" | "w1280" | "original";
export type logoSize = "w45" | "w92" | "w154" | "w185" | "w300" | "w500" | "original";
export type posterSize = "w92" | "w154" | "w185" | "w342" | "w500" | "w780" | "original";
export type profileSize = "w45" | "w185" | "h632" | "original";
export type stillSize = "w92" | "w185" | "w300" | "original";

export function tmdbImageUrl(path: string, quality: string = 'original') {
    return `https://image.tmdb.org/t/p/${quality}${path}`;
}

export async function useBackendFetch(url: string, options?: RequestInit, data?: Record<string, any>): Promise<Response> {
    const [user, _setUser, removeUser] = useLocalStorage<User | null>("user", null);
    if (user) {
        console.debug("Adding Authorization header to request", user);
        options = options || {};
        options.headers = { ...options.headers, 'Authorization': `Bearer ${user.token}` };
    }
    if (options?.method === 'POST' || options?.method === 'PUT' || options?.method === "PATCH") {
        console.debug("Adding Content-Type header to request", options);
        options.headers = { ...options.headers, 'Content-Type': 'application/json' };
        options.body = JSON.stringify(data);
    } else if (data) {
        console.debug("Adding query parameters to request", data);
        url += `?${new URLSearchParams(data).toString()}`;
    }
    console.debug("Fetching", url, options);
    const response = await fetch(`${BACKEND_URL}${url}`, options);
    if (response.status === 401) {
        console.warn("Received 401 from backend, logging out");
        removeUser();
    }
    return response;
}
