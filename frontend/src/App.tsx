
import './App.css';
import { MovieList } from './MovieCard';
import { MoviePage } from './MoviePage';

const example = {
    "adult": false,
    "backdrop_path": "/vL5LR6WdxWPjLPFRLe133jXWsh5.jpg",
    "genre_ids": [28, 12, 14, 878],
    "id": 19995,
    "original_language": "en",
    "original_title": "Avatar",
    "overview": "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
    "popularity": 155.426,
    "poster_path": "/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
    "release_date": "2009-12-15",
    "title": "Avatar",
    "video": false,
    "vote_average": 7.58,
    "vote_count": 30834
};

export default function App() {
    return <MovieList />;
}

// export default function App() {
//     return <MoviePage {...example} />;
// }