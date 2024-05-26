
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import MovieList from './pages/MovieList';
import { MoviePage } from './pages/MoviePage';

export default function App() {
    return (
        <ErrorBoundary>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<MovieList />} />
                    <Route path="/movie/:id" element={<MoviePage />} />
                </Routes>
            </BrowserRouter>
        </ErrorBoundary>
    )
}
