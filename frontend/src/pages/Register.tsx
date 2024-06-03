import { useCallback, useReducer, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDebounceCallback } from "usehooks-ts";
import { BACKEND_URL } from "../backend";
import "./RegisterLogin.css";

type formState = {
    usernameError?: string | null
    emailError?: string | null
    passwordError?: string | null
    password2Error?: string | null
    formError?: string | null
    isSubmitting: boolean
    isNew: boolean
}

export default function Register() {
    const [formState, setFormState] = useState<formState>({ isSubmitting: false, isNew: true });
    // TODO: Use useReducer to make it easier and more efficient for React but harder for us

    // Username field
    const usernameRef = useRef<HTMLInputElement>(null);
    const debounceDelay = import.meta.env.TEST ? 0 : 500;
    const usernameValidator = useDebounceCallback(async () => {
        const username = usernameRef.current?.value || "";
        if (username.length < 3) {
            setFormState(prev => ({ ...prev, isNew: false, usernameError: "Username must be at least 3 characters long" }));
            return;
        }
        const params = new URLSearchParams({ username });
        const response = await fetch(`${BACKEND_URL}/register/check?${params}`);
        if (!response.ok) {
            setFormState(prev => ({ ...prev, isNew: false, usernameError: "Username is not available" }));
            return;
        }
        // If we got here, the username is available, but we still want to set isNew to false, and we clear the error
        setFormState(prev => ({ ...prev, isNew: false, usernameError: null }));
    }, debounceDelay);
    const usernameErrorIcon = formState.isNew ? null : formState.usernameError ? "❌" : null;
    const usernameInput = <>
        <label htmlFor="username">Username{usernameErrorIcon && <span>{usernameErrorIcon}</span>}</label>
        <input type="text" name="username" id="username" ref={usernameRef} onChange={usernameValidator} required />
        {formState.usernameError && <div role="alert" className="error">{formState.usernameError}</div>}
    </>

    // Email field
    const emailRef = useRef<HTMLInputElement>(null);
    const emailValidator = () => {
        if (emailRef.current?.value.includes("@")) {
            setFormState(prev => ({ ...prev, isNew: false, emailError: null }));
        } else {
            setFormState(prev => ({ ...prev, isNew: false, emailError: "Invalid email address" }));
        }
    }
    const emailErrorIcon = formState.isNew ? null : formState.emailError ? "❌" : null;
    const emailInput = <>
        <label htmlFor="email">Email{emailErrorIcon && <span>{emailErrorIcon}</span>}</label>
        <input type="email" name="email" id="email" ref={emailRef} onChange={emailValidator} required />
        {formState.emailError && <div role="alert" className="error">{formState.emailError}</div>}
    </>

    // Password fields
    const passwordRef = useRef<HTMLInputElement>(null);
    const password2Ref = useRef<HTMLInputElement>(null);
    const passwordValidator = () => {
        const password = passwordRef.current?.value || "";
        const password2 = password2Ref.current?.value || "";
        if (password.length < 8) {
            setFormState(prev => ({ ...prev, isNew: false, passwordError: "Password must be at least 8 characters long" }));
        } else if (password && password !== password2) {
            setFormState(prev => ({ ...prev, isNew: false, passwordError: "Passwords do not match" }));
        } else {
            setFormState(prev => ({ ...prev, isNew: false, passwordError: null }));
        }
    }
    const passwordErrorIcon = formState.isNew ? null : formState.passwordError ? "❌" : null;
    const passwordInput = <>
        <label htmlFor="password">Password{passwordErrorIcon && <span>{passwordErrorIcon}</span>}</label>
        <input type="password" name="password" id="password" ref={passwordRef} onChange={passwordValidator} required />
        {formState.passwordError && <div role="alert" className="error">{formState.passwordError}</div>}
        <label htmlFor="password2">Confirm Password</label>
        <input type="password" name="password2" id="password2" ref={password2Ref} onChange={passwordValidator} required />
    </>

    const formValidation = () => {
        if (formState.isNew) return [false, false, false]
        const username = usernameRef.current?.value || "";
        const email = emailRef.current?.value || "";
        const password = passwordRef.current?.value || "";
        const password2 = password2Ref.current?.value || "";
        return [
            username.length > 3 && !formState.usernameError ? username : false,
            email.includes("@") && !formState.emailError ? email : false,
            password.length >= 8 && password === password2 && !formState.passwordError ? password : false,
        ]
    }

    const navigate = useNavigate();
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();  // Prevent the form from submitting the normal way (refreshing the page)
        console.debug("Submitting register form");
        setFormState(prev => ({ ...prev, isSubmitting: true }));
        setTimeout(() => {
            console.debug("Timeout expired, still waiting for response");
            setFormState(prev => ({ ...prev, formError: "Registration is taking longer than expected, if this continues please try again later" }));
        }, 10_000);  // 10 seconds timeout

        const [username, email, password] = formValidation();
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
            setFormState(prev => ({ ...prev, formError: "Registration failed, please try again later" }));
        }
    }

    const submitDisabled = formState.isNew || formState.isSubmitting || formValidation().includes(false);
    const submitText = formState.isSubmitting ? "Registering..." : "Register";
    return (
        <div className="register-form" >
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                {usernameInput}
                {emailInput}
                {passwordInput}
                {formState.formError && <div role="alert" className="error"></div>}
                <button type="submit" disabled={!!submitDisabled}>{submitText}</button>
                <Link to="/"><button type="reset">Go Back</button></Link>
            </form>
        </div>
    )
}
