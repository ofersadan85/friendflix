import { useLocalStorage } from "usehooks-ts";

export type User = {
    id: number;
    name: string;
    email: string;
    role: "admin" | "user";
    token?: string;
};

export function useCurrentUser() {
    // A more convenient hook to get the current user without the need to call useLocalStorage directly
    const [user, _setUser, _removeUser] = useLocalStorage<User | null>("user", null);
    return user;
}

export function useIsAdmin() {
    // A more convenient hook to check if the current user is an admin, if that's all we need
    const user = useCurrentUser();
    return user?.role === "admin";
}
