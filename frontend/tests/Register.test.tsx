import "@testing-library/jest-dom";
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { beforeAll, describe, expect, it, vi } from 'vitest';
import Register from '../src/pages/Register';

const checkUsernameAvailable = vi.fn(async (username: string) => username !== "taken")

beforeAll(() => {
    vi.mock('./path/to/module.js', () => {
        return { checkUsernameAvailable };
    })
});

describe(Register, () => {
    const renderForm = () => {
        render(<Register />);
        const title = screen.getByRole("heading", { name: /register/i });
        const username = screen.getByLabelText(/username/i);
        const email = screen.getByLabelText(/email/i);
        const password = screen.getByLabelText(/^password/i);
        const password2 = screen.getByLabelText(/confirm|repeat/i);
        const terms = screen.getByRole("checkbox");
        const submit = screen.getByRole("button");
        return { title, username, email, password, password2, terms, submit };
    }

    const getFormErrors = () => screen.queryAllByRole("listitem");

    it("Renders the register form with disabled submit", () => {
        const { title, username, email, password, password2, terms, submit } = renderForm();
        expect(title).toHaveTextContent(/register/i);
        expect(terms).not.toBeChecked();
        expect(submit).toBeDisabled();
        expect(getFormErrors()).toHaveLength(0);
    });

    it("Enables submit when form is valid", async () => {
        const { username, email, password, password2, terms, submit } = renderForm();
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
        await user.click(terms)
        
        expect(getFormErrors()).toHaveLength(0);
        expect(submit).toBeEnabled();
    });
});