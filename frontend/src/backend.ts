import { jwtDecode } from "jwt-decode";
import { useLocalStorage } from "usehooks-ts";
import { FullMovie, Movie } from "./types";
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


export async function useBackendFetch(url: string, options?: RequestInit, data?: Record<string, any>) {
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

export async function login(username_or_email: string, password: string) {
    const response = await fetch(`${BACKEND_URL}/login`, {
        method: 'POST',
        body: JSON.stringify({ username_or_email: username_or_email, password: password }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const { token } = await response.json();
    const user: User = {
        ...jwtDecode(token),
        token: token
    }
    const [_user, setUser, _removeUser] = useLocalStorage<User | null>("user", null);
    setUser(user);
}

export function register(username: string, email: string, password: string) {
    // TODO: Return the user object / token from the backend to skip the need for another login request
    return fetch(`${BACKEND_URL}/register`, {
        method: 'POST',
        body: JSON.stringify({ username, email, password }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

export function logout() {
    const [_user, _setUser, removeUser] = useLocalStorage<User | null>("user", null);
    removeUser();
    fetch(`${BACKEND_URL}/logout`);  // we don't care about the response, so no "await" or "return""
}

export async function checkUsernameAvailable(username: string): Promise<boolean> {
    if (username.length < 3) return false;
    const response = await useBackendFetch("/register/check/username", { method: 'GET' }, { username });
    return response.status === 200;
}

export function doMovieAction(movie_id: number, action: "like" | "play" | "watchlist") {
    // This function is not async, because we don't care about the response
    // We don't need to wait for the backend to respond before updating the UI
    // If we need to verify that the action was successful, we can do that later
    return useBackendFetch("/actions", { method: 'GET' }, { movie_id, action });
}

export async function getMovies(): Promise<Movie[]> {
    const response = await useBackendFetch("/movies");
    const data = await response.json();
    return data.results;
}

export async function getFullMovie(id: number): Promise<FullMovie> {
    const response = await useBackendFetch(`/movies/${id}`);
    const data = await response.json();
    return data;
}