import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from 'vitest';
import Register from '../src/pages/Register';
import { mockedFetch } from './setup';


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
        const usernameInput = screen.getByLabelText(/username/i);
        const emailInput = screen.getByLabelText(/email/i);
        const passwordInput = screen.getByLabelText(/^password/i);
        const password2Input = screen.getByLabelText(/confirm|repeat/i);
        const submit = screen.getByRole("button", { name: /submit|register/i });
        return { title, usernameInput, emailInput, passwordInput, password2Input, submit };
    }

    const getFormErrors = () => document.querySelectorAll(".error");

    const renderAndFillForm = async (username, email, password, password2) => {
        const {title, usernameInput, emailInput, passwordInput, password2Input, submit } = renderForm()
        const user = userEvent.setup();
        await user.click(usernameInput)
        await user.keyboard(username)
        await user.click(emailInput)
        await user.keyboard(email);
        await user.click(passwordInput)
        await user.keyboard(password);
        await user.click(password2Input)
        await user.keyboard(password2);
        return { title, usernameInput, emailInput, passwordInput, password2Input, submit, user };
    }

    it("Renders the register form with disabled submit", () => {
        const { title, submit } = renderForm();
        expect(title).toHaveTextContent(/register/i);
        expect(submit).toBeDisabled();
        expect(getFormErrors()).toHaveLength(0);
    });

    it("Enables submit when form is valid", async () => {
        const { submit } = await renderAndFillForm("adminUser", "admin@example.com", "12345678", "12345678");
        expect(getFormErrors()).toHaveLength(0);
        expect(submit).toBeEnabled();
    });

    it("Handles input validation for password fields", async () => {
        const { passwordInput, password2Input, submit, user } = await renderAndFillForm("adminUser", "admin@example.com", "1234567", "1234567");
        let errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/at least 8/i);
        expect(submit).toBeDisabled();
        await user.click(passwordInput)
        await user.keyboard("8");
        errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/match/i);
        expect(submit).toBeDisabled();
        await user.click(password2Input)
        await user.keyboard("8");
        errors = getFormErrors();
        expect(errors).toHaveLength(0);
        expect(submit).toBeEnabled();
    });

    it("Handles input validation for email field", async () => {
        const { emailInput, submit, user } = await renderAndFillForm("adminUser", "admin", "12345678", "12345678");
        let errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(errors[0]).toHaveTextContent(/invalid/i);
        expect(submit).toBeDisabled();
        await user.clear(emailInput);
        await user.keyboard("admin@example.com");
        errors = getFormErrors();
        expect(errors).toHaveLength(0);
        expect(submit).toBeEnabled();
    });

    it("Gives an error if the user already exists", async () => {
        const { usernameInput, submit, user } = await renderAndFillForm("taken", "admin@example.com", "12345678", "12345678");
        let errors = getFormErrors();
        expect(errors).toHaveLength(1);
        expect(submit).toBeDisabled();
        expect(mockedFetch).toHaveBeenCalled();
        mockedFetch.mockClear();
        await user.clear(usernameInput);
        await user.keyboard("nottaken");
        errors = getFormErrors();
        expect(errors).toHaveLength(0);
        expect(submit).toBeEnabled();
        expect(mockedFetch).toHaveBeenCalled();
    });
});
