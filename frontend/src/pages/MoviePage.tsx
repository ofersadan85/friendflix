import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { useLocalStorage } from "usehooks-ts";
import { backendFetch, tmdbImageUrl } from "../backend";
import { ActorCard, ActorCardSkeleton } from "../components/ActorCard";
import { Movie } from "../types";
import { User } from "../user";
import "./MoviePage.css";

export function MoviePageSkeleton() {
    const castSkeletons = Array(8).fill(<ActorCardSkeleton />)
    return (
        <div className="movie-page">
            <div className="backdrop-overlay"></div>
            <section className="info-section">
                <div className="movie-header">
                    <div className="movie-poster-skeleton" />
                    <h1></h1>
                </div>
                <div className="movie-buttons">
                    <button title="Play" disabled>▶️</button>
                    <button title="Add to Watchlist" disabled>➕</button>
                    <button title="Like" disabled>👍</button>
                </div>
                <h4></h4>
                <div className="movie-desc"></div>
                <div className="movie-social">
                    <ul>
                        <li>Stars: </li>
                        <li>Vote: </li>
                    </ul>
                </div>
                <div className="cast-cards">{castSkeletons}</div>
            </section>
            <Link to="/"><button>GO BACK</button></Link>
        </div>
    )

}

async function getMovie(id: number | string, removeUser: () => void): Promise<Movie | undefined> {
    const response = await backendFetch(`/movies/${id}`);
    if (response.status === 401) {
        removeUser();
        return;
    }
    return await response.json();
}

export function MoviePage() {
    const { id } = useParams();
    const movieId = parseInt(id || "");
    const { state } = useLocation();
    const [movie, setMovie] = useState<Movie | null>(state);
    const [user, _setUser, removeUser] = useLocalStorage<User | null>("user", null);

    if (!movie) return <MoviePageSkeleton />
    const credits = movie.credits || { cast: [] };
    const cast = credits.cast.slice(0, 10);
    const backdrop = tmdbImageUrl(movie.backdrop_path, "w780");
    const poster = tmdbImageUrl(movie.poster_path, "w342") || "";

    const backdropStyle: React.CSSProperties = {
        backgroundImage: `url(${backdrop})`,
    }

    const movieDate = new Date(movie.release_date);
    function doMovieAction(movie_id: number, action: "like" | "play" | "watchlist") {
        // This function is not async, because we don't care about the response
        // We don't need to wait for the backend to respond before updating the UI
        // If we need to verify that the action was successful, we can do that later
        backendFetch(`/actions`, user?.token, { method: 'POST' }, { movie_id, action });
    }

    useEffect(() => {
        getMovie(movieId, removeUser).then(data => setMovie(data || null));
    }, [id, user]);

    return (
        <div className="movie-page" style={backdropStyle}>
            <div className="backdrop-overlay"></div>
            <section className="info-section">
                <div className="movie-header">
                    <img className="movie-poster" src={poster} alt={movie.title} />
                    <h1>{movie.title}</h1>
                </div>
                <div className="movie-buttons">
                    <button title="Play" onClick={() => doMovieAction(movieId, "play")}>▶️</button>
                    <button title="Add to Watchlist" onClick={() => doMovieAction(movieId, "watchlist")}>➕</button>
                    <button title="Like" onClick={() => doMovieAction(movieId, "like")}>👍</button>
                </div>
                <h4>{movieDate.getFullYear()}</h4>
                <div className="movie-desc">{movie.overview}</div>
                <div className="movie-social">
                    <ul>
                        <li>Stars: {movie.vote_average}</li>
                        <li>Vote: {movie.vote_count}</li>
                    </ul>
                </div>
                {cast && <div className="cast-cards">{cast.map(ActorCard)}</div>}
            </section>
            <Link to="/"><button>GO BACK</button></Link>
        </div>
    )
}
