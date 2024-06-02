import "@testing-library/jest-dom";
import { afterAll, beforeAll, vi } from 'vitest';

export const mockedFetch = vi.fn(async (path: string) => {
    if (path.includes("/register/check")) {
        if (path.includes("username=taken")) {
            return { ok: false }
        } else {
            return { ok: true }
        }
    } else {
        return { ok: true, json: () => ({ results: [] })}
    }
})

beforeAll(() => {
    vi.stubGlobal("fetch", mockedFetch)
})

afterAll(() => {
    vi.unstubAllGlobals()
})
