
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import NavBar from './components/NavBar';
import Login, { Logout } from './pages/Login';
import MovieList from './pages/MovieList';
import { MoviePage } from './pages/MoviePage';
import Register from './pages/Register';
import UserPage from './pages/UserPage';
import { useCurrentUser } from './user';

export default function App() {
    const [user] = useCurrentUser();
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
                    <Route path="/user/:userId" element={<UserPage />} />
                    <Route path="/user" element={<Navigate to={user ? `/user/${user.id}` : "/"} />} />
                    <Route path="/profile" element={<Navigate to={user ? `/user/${user.id}` : "/"} />} />
                </Routes>
            </BrowserRouter>
        </ErrorBoundary>
    )
}
