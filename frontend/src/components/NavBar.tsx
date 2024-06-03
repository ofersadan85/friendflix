import { Link } from "react-router-dom";
import { useLocalStorage } from "usehooks-ts";
import { User } from "../user";
import "./NavBar.css";

function UserNavBar() {
    return <>
        <li><Link to="/logout">Logout</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/settings">Settings</Link></li>
    </>
}

function AdminNavBar() {
    return <>
        <li><Link to="/admin">Admin</Link></li>
        <li><Link to="/users">Users</Link></li>
    </>
}

function GuestNavBar() {
    return <>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/register">Register</Link></li>
    </>
}

export default function NavBar() {
    const [user, _setUser, _removeUser] = useLocalStorage<User | null>("user", null);
    return (
        <nav className="navbar-top">
            <ul>
                <li><Link to="/">Home</Link></li>
                <li className="separator"></li>
                {user?.role === "admin" && <AdminNavBar />}
                {user ? <UserNavBar /> : <GuestNavBar />}
            </ul>
        </nav>
    );
}
