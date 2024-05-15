import { createContext, useContext, useState } from "react";

const ctx = createContext<[string | null, React.Dispatch<React.SetStateAction<string | null>>, () => void] | null>(null);

type MovieCtxProps = {
    children: JSX.Element[] | JSX.Element
}

export function LastMovieContext(properties: MovieCtxProps) {
    const [lastMovie, setLastMovie] = useState<null | string>(null);
    function clearLastMovie() {
        console.log("Warning: clearing last movie");
        setLastMovie(null);
    }
    return <ctx.Provider value={[lastMovie, setLastMovie, clearLastMovie]}>
        {properties.children}
    </ctx.Provider>

}

export function useLastMovie() {
    return useContext(ctx);
}
