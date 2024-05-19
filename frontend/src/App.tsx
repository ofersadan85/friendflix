
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import MovieList from './pages/MovieList';
import { MoviePage } from './pages/MoviePage';

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MovieList />} />
                <Route path="/movie/:id" element={<MoviePage />} />
            </Routes>
        </BrowserRouter>
    )
}
