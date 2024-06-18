import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useLocalStorage } from "usehooks-ts";
import { backendFetch } from "../backend";
import { useCurrentUser } from "../user";

type UserActionCountPanelProps = {
    userId: number;
    action: "watchlist" | "played" | "watched" | "rated" | "reviewed" | "liked" | "disliked" | "commented" | "shared";
}

export function UserActionCounterPanel({ userId, action }: UserActionCountPanelProps) {
    const [user, _setUser, removeUser] = useCurrentUser();
    const [movieIds, setMovieIds] = useLocalStorage<number[]>(action, []);
    const isViewingSelf = user?.id === userId;
    const fetchUserActions = async () => {
        if (!user) setMovieIds([]);
        const response = await backendFetch(`/user/${userId}/${action}`, user?.token);
        if (response.status === 401) removeUser();
        if (response.ok) {
            const data = await response.json();
            if (isViewingSelf) setMovieIds(data);
        }
    }

    useEffect(() => {
        fetchUserActions();
    }, [user, action])

    const actionList = action.endsWith("list") ? action : action + " list";
    if (!user) return null;
    const link = <Link to={`/user/${user.id}/${action}`}>{actionList}</Link>
    let text;
    if (isViewingSelf && movieIds.length === 0) {
        text = <>Your {link} is empty. Add some movies!</>;
    } else if (isViewingSelf && movieIds.length > 0) {
        text = <>You have {movieIds.length} movies in your {link}.</>;
    } else if (!isViewingSelf && movieIds.length === 0) {
        text = <>This user has no movies in their {link}</>;
    } else if (!isViewingSelf && movieIds.length > 0) {
        text = <>They have {movieIds.length} movies in their {link}</>;
    } else {
        console.error("This should never happen");
        text = <></>;
    }

    return <h4 className={`user-action-counter ${action}`}>{text}</h4>
}
