import { useEffect, useState } from "react";
import { getMovies } from "../tmdb";
import { Movie } from "../types";
import MovieCard from "../components/MovieCard";
import './MovieList.css';

export default function MovieList() {
    const [movies, setMovies] = useState<Movie[]>([]);
    useEffect(() => {
        getMovies().then(movies => setMovies(movies));
    }, []);

    const movieCards = movies.length === 0 ? <h1>Loading...</h1> : movies.map(movie => <MovieCard key={movie.id} watched {...movie} />);

    return (
        <section className="movie-section">
            <h2>Most popular movies</h2>
            <div className="movie-list">
                {movieCards}
            </div>
        </section>
    )
};
