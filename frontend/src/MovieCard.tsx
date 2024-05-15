
import  { useState, useEffect } from 'react';
import {Movie} from './Typs.tsx';
import './card.css';

function MovieCard() {
    const [selectMovie, setSelectMovie] = useState<Movie[]>([]);

    useEffect(() => {
        const get_movie = () => {
            fetch('https://api.themoviedb.org/3/discover/movie?&sort_by=revenue.desc&api_key=ffe5c55abd58ac422555285b6b0f1e30')
                .then(response => response.json())
                .then((data )=> {
                    const MovieObject =  data.results;
                    setSelectMovie(MovieObject);
                    console.log(MovieObject)
                })
                .catch(error => {
                    console.error('Error fetching movie data:', error);
                });
        }

        get_movie();
    }, []);

    return (
        <>
            {selectMovie.map((movie) => (
                <div className="movie_card" id="bright" key={movie.id}>
                    <div className="info_section">
                        <div className="movie_header">
                            <img className="locandina" src={movie.poster_path} alt={movie.title} />
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
                    <div className="blur_back bright_back"></div>
                </div>
            ))}
        </>
    );
    
}

export default MovieCard;