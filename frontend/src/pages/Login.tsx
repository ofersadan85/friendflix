import { jwtDecode } from "jwt-decode";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "usehooks-ts";
import { BACKEND_URL, backendFetch } from "../backend";
import { User } from "../user";
import "./RegisterLogin.css";

export default function Login() {
    const [user, setUser] = useLocalStorage<User | null>("user", null);
    const usernameRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);
    const [formError, setFormError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const navigate = useNavigate();
    const params = new URLSearchParams(window.location.search);
    if (user) navigate("/");
    if (params.get("registered") && formError === null) setFormError("Registration successful! Please log in");

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        console.log("Logging in...");
        setIsSubmitting(true);
        let response;
        try {
            response = await fetch(`${BACKEND_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: usernameRef.current?.value || "",
                    password: passwordRef.current?.value || "",
                }),
            });
        } catch (error) {
            console.error("Failed to login", error);
            setFormError("Failed to login, please try again");
            setIsSubmitting(false);
            return;
        }
        if (response.ok) {
            const data = await response.json();
            try {
                const user: User = { token: data.token, ...jwtDecode(data.token) };
                setUser(user);
                navigate("/");
            } catch (error) {
                console.error("Failed to decode token", error);
                setFormError("Login failed, please try again");
                setIsSubmitting(false);
            }
        } else if (response.status === 401) {
            console.error("Login failed, invalid credentials");
            setFormError("Invalid username or password");
            setIsSubmitting(false);
        } else {
            console.error("Login failed", response, await response.text());
            setFormError("Login failed for unknown reason, please try again");
            setIsSubmitting(false);
        }
    }

    const submitText = isSubmitting ? "Logging in..." : "Login";
    const submitDisabled = isSubmitting;

    return (
        <div className="login-form">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input type="text" name="username" id="username" ref={usernameRef} required />
                <label htmlFor="password">Password</label>
                <input type="password" name="password" id="password" ref={passwordRef} required />
                <button type="submit" disabled={submitDisabled}>{submitText}</button>
                {formError && <div role="alert" className="error">{formError}</div>}
            </form>
        </div>
    );
}

export function Logout() {
    const [user, _setUser, removeUser] = useLocalStorage<User | null>("user", null);
    const navigate = useNavigate();
    useEffect(() => {
        backendFetch("/logout", user?.token);  // we don't care about the response, so no "await" or "return""
        removeUser();
        navigate("/");
    }, []);
    return null;
}
