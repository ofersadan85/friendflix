import "@testing-library/jest-dom";
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { beforeAll, describe, expect, it, vi } from 'vitest';
import Register from '../src/pages/Register';
import { MemoryRouter, Route, Routes } from "react-router-dom";

const checkUsernameAvailable = vi.fn(async (username: string) => username !== "taken")

beforeAll(() => {
    vi.mock('./path/to/module.js', () => {
        return { checkUsernameAvailable };
    })
});

describe(Register, () => {
    const renderForm = () => {
        render(
            <MemoryRouter>
                <Routes>
                    <Route path="/" element={<Register />} />
                </Routes>
            </MemoryRouter>
        )
        const title = screen.getByRole("heading", { name: /register/i });
        const username = screen.getByLabelText(/username/i);
        const email = screen.getByLabelText(/email/i);
        const password = screen.getByLabelText(/^password/i);
        const password2 = screen.getByLabelText(/confirm|repeat/i);
        const submit = screen.getByRole("button", { name: /submit|register/i });
        return { title, username, email, password, password2, submit };
    }

    const getFormErrors = () => document.querySelectorAll(".error");

    it("Renders the register form with disabled submit", () => {
        const { title, submit } = renderForm();
        expect(title).toHaveTextContent(/register/i);
        expect(submit).toBeDisabled();
        expect(getFormErrors()).toHaveLength(0);
    });

    it("Enables submit when form is valid", async () => {
        const { username, email, password, password2, submit } = renderForm();
        const user = userEvent.setup()
        expect(submit).toBeDisabled();
        await user.click(username)
        await user.keyboard("abcd1234")
        await user.click(email)
        await user.keyboard("test@example.com");
        await user.click(password)
        await user.keyboard("password123");
        await user.click(password2)
        await user.keyboard("password123");

        expect(getFormErrors()).toHaveLength(0);
        expect(submit).toBeEnabled();
    });

    it("Handles input validation for password fields", async () => {
        const { password, password2, submit } = renderForm();
        let errors = getFormErrors();
        expect(errors).toHaveLength(0);
        const user = userEvent.setup()
        await user.click(password)
        await user.keyboard("1234567")
        errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/at least 8/i);
        expect(submit).toBeDisabled();
        await user.keyboard("8");
        errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/match/i);
        expect(submit).toBeDisabled();
        await user.click(password2)
        await user.keyboard("password123");
        errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/match/i);
        expect(submit).toBeDisabled();
        await user.clear(password2);
        await user.keyboard("12345678");
        errors = getFormErrors();
        expect(errors).toHaveLength(0);
        expect(submit).toBeDisabled(); // Still disabled because username and email are missing
    });

    it("Handles input validation for email field", async () => {
        const { email, submit } = renderForm();
        let errors = getFormErrors();
        expect(errors).toHaveLength(0);
        const user = userEvent.setup()
        await user.click(email)
        await user.keyboard("invalid-email");
        errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/invalid/i);
        expect(submit).toBeDisabled();
        await user.clear(email);
        await user.keyboard("@example.com");
        errors = getFormErrors();
        expect(errors).toHaveLength(0);
        expect(submit).toBeDisabled(); // Still disabled because username and password are missing
    });

    // TODO: Add tests for username validation with mocked fetch to backend
});