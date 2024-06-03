
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import NavBar from './components/NavBar';
import Login, { Logout } from './pages/Login';
import MovieList from './pages/MovieList';
import { MoviePage } from './pages/MoviePage';
import Register from './pages/Register';

export default function App() {
    return (
        <ErrorBoundary>
            <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path="/" element={<MovieList />} />
                    <Route path="/movie/:id" element={<MoviePage />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/logout" element={<Logout />} />
                </Routes>
            </BrowserRouter>
        </ErrorBoundary>
    )
}
