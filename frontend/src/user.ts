import { useEffect } from "react";
import { useLocalStorage } from "usehooks-ts";

export type User = {
    id: number;
    username: string;
    email: string;
    role: "admin" | "user";
    token?: string;
    exp?: number;
};

export function useCurrentUser() {
    // A more convenient hook to get the current user without the need to call useLocalStorage directly
    const [user, setUser, removeUser] = useLocalStorage<User | null>("user", null);
    const expired = user?.exp && user.exp < Date.now() / 1000;
    useEffect(() => {
        if (expired) {
            console.debug("User token expired, removing user");
            removeUser();
        }
    }, [user]);
    return [expired ? null : user, setUser, removeUser] as const;
}
