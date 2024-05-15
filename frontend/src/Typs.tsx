export type Movie = {
    id: number;
    isAdult: boolean;
    poster_path: string;
    original_language: "en" | "hb" | "ru";
    title: string;
    release_date: string;
    vote_average: number;
    overview: string;
    vote_count: number;
}