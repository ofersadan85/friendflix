export type Movie = {
    id: number;
    isAdult: boolean;
    poster_path: string;
    backdrop_path: string;
    original_language: "en" | "hb" | "ru";
    title: string;
    release_date: string;
    vote_average: number;
    overview: string;
    vote_count: number;
    watched: boolean;
    genre_ids?: number[];
    genres?: Genre[];
    credits?: { cast: Actor[] };
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
