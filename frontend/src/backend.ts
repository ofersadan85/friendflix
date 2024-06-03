
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL as string;

export type backdropSize = "w300" | "w780" | "w1280" | "original";
export type logoSize = "w45" | "w92" | "w154" | "w185" | "w300" | "w500" | "original";
export type posterSize = "w92" | "w154" | "w185" | "w342" | "w500" | "w780" | "original";
export type profileSize = "w45" | "w185" | "h632" | "original";
export type stillSize = "w92" | "w185" | "w300" | "original";

export function tmdbImageUrl(path: string, quality: string = 'original') {
    return `https://image.tmdb.org/t/p/${quality}${path}`;
}

export async function backendFetch(url: string, token?: string, options?: RequestInit, data?: Record<string, any>): Promise<Response> {
    if (token) {
        options = options || {};
        options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };
    }
    if (options?.method === 'POST' || options?.method === 'PUT' || options?.method === "PATCH") {
        console.debug("Adding Content-Type header to request", options);
        options.headers = { ...options.headers, 'Content-Type': 'application/json' };
        options.body = JSON.stringify(data);
    } else if (data) {
        console.debug("Adding query parameters to request", data);
        url += `?${new URLSearchParams(data).toString()}`;
    }
    if (!import.meta.env.PROD) console.debug("Fetching", url, options);
    const response = await fetch(`${BACKEND_URL}${url}`, options);
    return response;
}
