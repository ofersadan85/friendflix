import { useEffect, useState } from "react";
import { Actor, FullMovie } from "./types";
import './card.css';
import { Link, useParams } from "react-router-dom";
import { useLastMovie } from "./lastMovieCtx";


function ActorCard(actor: Actor) {
    const imageQuality = "w185";
    const imageUrl = `https://image.tmdb.org/t/p/${imageQuality}${actor.profile_path}`;
    return <div className="actorInfo" key={actor.id}>
        <img className="actorImage" src={imageUrl} />
        <div className="actorName">{actor.name}</div>
        <div className="actorCharacter">{actor.character}</div>
    </div>
}

export function MoviePage() {
    // const params = useParams();
    // const id = params.id;
    const { id } = useParams();
    const [data, setData] = useState<FullMovie | null>(null);
    const [lastMovie, setLastMovie, clearLastMovie] = useLastMovie();


    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/movie/${id}?append_to_response=credits&language=en-US&api_key=ffe5c55abd58ac422555285b6b0f1e30`)
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => {
                console.error('Error fetching movie data:', error);
            });
    }, [id]);

    const cast = data && data.credits.cast.slice(0, 10);
    const backdropQuality = "w780";
    const backdrop = data && `https://image.tmdb.org/t/p/${backdropQuality}${data.backdrop_path}`;;
    const posterQuality = "w780";
    const full_poster_path = data ? `https://image.tmdb.org/t/p/${posterQuality}${data.poster_path}` : "";

    if (!data) {
        return <h1>No data</h1>
    } else {
        setLastMovie(data.title);
    }

    return <div className="moviePage">
        <h2>The last movie you watched was {lastMovie}</h2>
        <div className="info_section">
            <div className="movie_header">
                <img className="locandina" src={full_poster_path} alt={data.title} />
                <h1>{data.title}</h1>
                <h4>{data.release_date}</h4>
            </div>
            <div className="movie_desc">
                <p className="text">
                    {data.overview}
                </p>
            </div>
            <div className="movie_social">
                <ul>
                    <li><i className="fa fa-star"></i> Stars: {data.vote_average}</li>
                    <li><i className="fa fa-thumbs-up"></i> Vote: {data.vote_count}</li>
                </ul>
            </div>
        </div>
        {cast && <div className="castCards">{cast.map(ActorCard)}</div>}
        <div className="blur_back bright_back"></div>
        {backdrop && <img className="movieBackdrop" src={backdrop} />}
        <Link to="/"><button>GO BACK</button></Link>
    </div>
}