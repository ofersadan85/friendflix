const BASE_URL = 'http://127.0.0.1:5000';

export type backdropSize = "w300" | "w780" | "w1280" | "original";
export type logoSize = "w45" | "w92" | "w154" | "w185" | "w300" | "w500" | "original";
export type posterSize = "w92" | "w154" | "w185" | "w342" | "w500" | "w780" | "original";
export type profileSize = "w45" | "w185" | "h632" | "original";
export type stillSize = "w92" | "w185" | "w300" | "original";

export function tmdbImageUrl(path: string, quality: string = 'original') {
    return `https://image.tmdb.org/t/p/${quality}${path}`;
}

export function doMovieAction(movie_id: number, action: "like" | "play" | "watchlist") {
    return fetch(`${BASE_URL}/actions?movie_id=${movie_id}&action=${action}`)
}

export function getMovies() {
    return fetch(`${BASE_URL}/movies`)
        .then(response => response.json())
        .then(data => data.results)
        .catch(error => {
            console.error('Error fetching movie data:', error);
        });
}

export function getFullMovie(id: number) {
    return fetch(`${BASE_URL}/movies/${id}`)
        .then(response => response.json())
        .catch(error => {
            console.error('Error fetching movie data:', error);
        });
}