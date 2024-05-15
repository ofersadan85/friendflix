import { useEffect, useState } from "react";
import { Actor, FullMovie, Movie } from "./types";
import './card.css';


function ActorCard(actor: Actor) {
    const imageQuality = "w185";
    const imageUrl = `https://image.tmdb.org/t/p/${imageQuality}${actor.profile_path}`;
    return <div className="actorInfo" key={actor.id}>
        <img className="actorImage" src={imageUrl} />
        <div className="actorName">{actor.name}</div>
        <div className="actorCharacter">{actor.character}</div>
    </div>
}

export function MoviePage(movie: Movie) {
    const [data, setData] = useState<FullMovie | null>(null)
    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/movie/${movie.id}?append_to_response=credits&language=en-US&api_key=ffe5c55abd58ac422555285b6b0f1e30`)
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => {
                console.error('Error fetching movie data:', error);
            });
    }, [movie]);

    const cast = data && data.credits.cast.slice(0, 10);
    const backdropQuality = "w780";
    const backdrop = data && `https://image.tmdb.org/t/p/${backdropQuality}${data.backdrop_path}`;;
    const posterQuality = "w780";
    const full_poster_path = `https://image.tmdb.org/t/p/${posterQuality}${movie.poster_path}`;

    return <div className="moviePage">
        <div className="info_section">
            <div className="movie_header">
                <img className="locandina" src={full_poster_path} alt={movie.title} />
                <h1>{movie.title}</h1>
                <h4>{movie.release_date}</h4>
            </div>
            <div className="movie_desc">
                <p className="text">
                    {movie.overview}
                </p>
            </div>
            <div className="movie_social">
                <ul>
                    <li><i className="fa fa-star"></i> Stars: {movie.vote_average}</li>
                    <li><i className="fa fa-thumbs-up"></i> Vote: {movie.vote_count}</li>
                </ul>
            </div>
        </div>
        {cast && <div className="castCards">{cast.map(ActorCard)}</div>}
        <div className="blur_back bright_back"></div>
        {backdrop && <img className="movieBackdrop" src={backdrop} />}
    </div>
}