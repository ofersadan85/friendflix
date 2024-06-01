import { useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../backend";
import { ValidatedInput, ValidatedInputRef } from "../components/ValidatedInput";
import "./Register.css";


export default function Register() {
    console.debug("Rendering Register form");
    const formRef = useRef<HTMLFormElement>(null);
    const [formErrors, setFormErrors] = useState<string[]>([""]);

    const usernameRef = useRef<ValidatedInputRef>(null);
    const emailRef = useRef<ValidatedInputRef>(null);
    const passwordRef = useRef<ValidatedInputRef>(null);
    const password2Ref = useRef<ValidatedInputRef>(null);
    const navigate = useNavigate();
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();  // Prevent the form from submitting the normal way (refreshing the page)
        console.debug("Submitting register form");
        setTimeout(() => {
            console.debug("Timeout expired, still waiting for response");
            // TODO: Show a message to the user that the request is taking longer than expected
        }, 10_000);

        const username = usernameRef.current?.value()
        const email = emailRef.current?.value()
        const password = passwordRef.current?.value()
        const response = await fetch(`${BACKEND_URL}/register`, {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            console.debug("Registration successful");
            navigate("/login?registered=true");
        } else {
            console.error("Registration failed", response, await response.text());
            // TODO: Show an error message to the user
        }
    }
    const usernameValidator = async (v: string) => {
        if (v.length < 3) return "Username must be at least 3 characters long";
        const params = new URLSearchParams({ username: v });
        const response = await fetch(`${BACKEND_URL}/register/check?${params}`);
        return response.ok ? null : "Username is not available";
    }
    const emailValidator = (v: string) => v.includes("@") ? null : "Invalid email address";
    const passwordValidator = (v: string) => v.length < 8 ? "Password must be at least 8 characters long" : null;
    const passwordMatchValidator = () => passwordRef.current?.value() === password2Ref.current?.value() ? null : "Passwords do not match";

    const changeHandler = () => {
        console.debug("Form changed");
        const errors = [usernameRef, emailRef, passwordRef, password2Ref].map(ref => ref.current?.error()).filter(e => e);
        setFormErrors(errors as string[]);
        console.debug("Form errors", errors);
    }
    const submitDisabled = formErrors.length > 0;
    return (
        <div className="register-form" >
            <h2>Register</h2>
            <form onSubmit={handleSubmit} onChange={changeHandler} ref={formRef}>
                <ValidatedInput type="text" label="Username" validator={usernameValidator} debounce={500} ref={usernameRef} />
                <ValidatedInput type="email" label="Email" validator={emailValidator} ref={emailRef} />
                <ValidatedInput type="password" label="Password" validator={passwordValidator} ref={passwordRef} />
                <ValidatedInput type="password" label="Confirm Password" name="password2" validator={passwordMatchValidator} ref={password2Ref} />
                <div role="alert" className="error"></div>
                <button type="submit" disabled={submitDisabled}>Register</button>
                <Link to="/"><button type="reset">Go Back</button></Link>
            </form>
        </div>
    )
}