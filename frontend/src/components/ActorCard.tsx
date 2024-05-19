import { tmdbImageUrl } from "../tmdb";
import { Actor } from "../types";
import "./ActorCard.css";

export function ActorCard(actor: Actor) {
    const profileImage = tmdbImageUrl(actor.profile_path, "w185");
    return <div className="actor-info" key={actor.id}>
        <img className="actor-image" src={profileImage} />
        <div className="actor-name">{actor.name}</div>
        <div className="actor-character">{actor.character}</div>
    </div>
}
