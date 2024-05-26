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
    watched: boolean;
}

export type Genre = {
    id: number
    name: string
}

export type Actor = {
    id: number
    name: string
    profile_path: string,
    character: string,
}

export type FullMovie = Movie & {
    backdrop_path: string
    genres: Genre[]
    credits: { cast: Actor[] }
}