
import { useState } from 'react';
import './App.css';
import { MovieList } from './MovieCard';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MoviePage } from './MoviePage';


export default function App() {
    return <BrowserRouter>
        <Routes>
            <Route path="/" element={<MovieList />} />
            <Route path="/movie/:id" element={<MoviePage />} />
        </Routes>
    </BrowserRouter>

}
