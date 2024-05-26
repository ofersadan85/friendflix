import { useEffect, useState } from "react";
import { getMovies } from "../backend";
import { ErrorBoundary } from "../components/ErrorBoundary";
import MovieCard, { MovieCardSkeleton } from "../components/MovieCard";
import { Movie } from "../types";
import './MovieList.css';

function MovieListError() {
    return <>
        <h1>Something went wrong displaying the movie list</h1>
        <p>Please try again</p>
        <button onClick={window.history.back} title="Go back">Go back</button>
    </>
}

export default function MovieList() {
    const [movies, setMovies] = useState<Movie[]>([]);
    useEffect(() => {
        getMovies().then(movies => setMovies(movies));
    }, []);

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
