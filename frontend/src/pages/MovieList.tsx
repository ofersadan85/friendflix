import { useEffect, useState } from "react";
import { useLocalStorage } from "usehooks-ts";
import { backendFetch } from "../backend";
import { ErrorBoundary } from "../components/ErrorBoundary";
import MovieCard, { MovieCardSkeleton } from "../components/MovieCard";
import { Movie } from "../types";
import { User } from "../user";
import './MovieList.css';

function MovieListError() {
    return <>
        <h1>Something went wrong displaying the movie list</h1>
        <p>Please try again</p>
        <button onClick={window.history.back} title="Go back">Go back</button>
    </>
}

async function getMovies(removeUser: () => void): Promise<Movie[] | undefined> {
    const response = await backendFetch("/movies/top");
    if (response.status === 401) {
        removeUser();
        return;
    }
    const data = await response.json();
    return data.results;
}

export default function MovieList() {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [user, _setUser, removeUser] = useLocalStorage<User | null>("user", null);
    useEffect(() => {
        getMovies(removeUser).then(data => setMovies(data || []));
    }, [user]);

    const skeletons = Array(8).fill(<MovieCardSkeleton />)

    return (
        <ErrorBoundary fallback={<MovieListError />}>
            <section className="movie-section">
                <h2>Most popular movies</h2>
                <div className="movie-list">
                    {movies.length === 0 ? skeletons : movies.map(movie => <MovieCard key={movie.id} {...movie} />)}
                </div>
            </section>
        </ErrorBoundary>
    )
};
