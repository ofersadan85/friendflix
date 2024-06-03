import "@testing-library/jest-dom";
import { render, screen } from '@testing-library/react';
import React from 'react';
import { describe, expect, it } from 'vitest';
import MovieList from '../src/pages/MovieList';

describe(MovieList, () => {
    it("Renders the default movie list", () => {
        render(<MovieList />)
        const title = screen.getByRole("heading", {name: /movies/i});
        expect(title).toHaveTextContent(/movies/i);
    });
});
