import { Link } from "react-router-dom";
import { tmdbImageUrl } from "../backend";
import { Movie } from "../types";
import './MovieCard.css';

type MovieCardProps = Movie & { watched: boolean };

export function MovieCardSkeleton() {
    return (
        <div className="movie-card-skeleton">
            <div className="movie-poster"></div>
            <div className="movie-info">
                <h3></h3>
                <p></p>
            </div>
        </div>
    )
}

export default function MovieCard({ id, title, release_date, poster_path, watched }: MovieCardProps) {
    const poster = tmdbImageUrl(poster_path, "w154");
    watched = Math.random() > 0.5;  // TODO: Actually implement this feature
    return (
        <Link to={`/movie/${id}`}>
            <div className="movie-card">
                {watched && <div className="watched-overlay">✅</div>}
                <img src={poster} alt={title} />
                <div className="movie-info">
                    <h3>{title}</h3>
                    <p>{release_date}</p>
                </div>
            </div>
        </Link>
    )
}
