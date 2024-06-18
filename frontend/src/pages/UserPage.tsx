import { Navigate, useParams } from "react-router-dom";
import { UserActionCounterPanel } from "../components/UserActionCountPanel";
import { useCurrentUser } from "../user";

export default function UserPage() {
    const [user] = useCurrentUser();
    const userId = parseInt(useParams().userId || "");
    console.debug(`User ${user?.id} is viewing user page for ${userId}`);
    if (!userId) return <Navigate to="/" />;
    const isViewingSelf = user?.id === userId;
    const addFriend = () => {
        if (!user) return <Navigate to="/login" />;
        // TODO: Implement add friend
        console.log(`${user?.id} adding friend ${userId}`)
    }
    const panels = isViewingSelf ? // TODO: Add panels only if user is sharing them publicly
        <div user-actions-container>
            <UserActionCounterPanel userId={userId} action="watchlist" /><hr />
            <UserActionCounterPanel userId={userId} action="played" /><hr />
            <UserActionCounterPanel userId={userId} action="rated" /><hr />
            <UserActionCounterPanel userId={userId} action="reviewed" /><hr />
            <UserActionCounterPanel userId={userId} action="liked" /><hr />
            <UserActionCounterPanel userId={userId} action="disliked" /><hr />
            <UserActionCounterPanel userId={userId} action="commented" /><hr />
            <UserActionCounterPanel userId={userId} action="shared" />
        </div> :
        <div user-actions-container>
            <p>This user has not shared their activity</p>
            <button onClick={addFriend}>Add friend</button>
        </div>;

    return (
        <div>
            <h1>{user?.username}</h1>
            <p>{user?.email}</p>
            {panels}
        </div>
    );
}
