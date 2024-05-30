# FriendFlix

This is a demo project for watching and sharing movies and TV episodes with friends.

## Usage

To run the project locally, follow these steps:

```bash
git clone https://github.com/ofersadan85/friendflix
cd friendflix
```

### Backend API Server (Flask)

Build the backend dependencies. Make sure to run the following commands in the `backend` directory (and it's recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

This project must have a valid API key for TMDB. Copy the file [backend/example.env](backend/example.env) to `backend/.env` and replace the placeholder for `TMDB_API_KEY` with a valid API key.

After that, you can run the backend server (inside the `backend` directory):

```bash
flask run
```

The backend server will be running at [http://localhost:5000](http://localhost:5000) (the port number may change, check the output of the `flask run` command).

If you need to run the backend tests you first need to install the test / dev dependencies:

```bash
pip install -r requirements-dev.txt
pytest
```

### Frontend (React / Vite / TypeScript)

From within the [frontend](frontend) directory, run the following commands:

```bash
npm install
npm run dev
```

You should be able to access the project at [http://localhost:5173](http://localhost:5173) in your browser (the port may change, check the output of the `npm run dev` command).

You can also run the frontend tests:

```bash
npm run test
```

### Database

The backend uses SQLite as the database. The database file is created automatically when the backend server is started. If it didn't, or if you need to reset the database, you can delete the `backend/db/db.sqlite` file and restart the backend server. The database will be recreated.

Alternatively, you can run the following command to create the database file:

```bash
python db/db.py
```

## Running the Project with Docker

This part will be updated soon. [//]: # (TODO)

## VsCode shortcuts

This project has some shortcuts for VsCode that can be used to run the tests and the development servers, for easier development. You can find them in [.vscode/tasks.json](.vscode/tasks.json). Run Ctrl+Shift+P and type "Tasks: Run Task" to see the available tasks. For example, running the "DEV Server" task will start the frontend development server and the backend server on a split terminal.

## CI/CD

[![Frontend Tests](https://github.com/ofersadan85/friendflix/actions/workflows/react_tests.yml/badge.svg)](https://github.com/ofersadan85/friendflix/actions/workflows/react_tests.yml)
[![Backend Tests](https://github.com/ofersadan85/friendflix/actions/workflows/python_tests.yml/badge.svg)](https://github.com/ofersadan85/friendflix/actions/workflows/python_tests.yml)

This project uses GitHub Actions for CI/CD. The workflow files can be found in the [.github/workflows](.github/workflows) directory. Both the frontend tests and the backend tests are run on every push to the `main` branch and on every pull request to the `main` branch, but both only run on changes to their respective directories.

CD (Continuous Deployment to a production server) is not set up yet. [//]: # (TODO)

## License

This project is free and open source, and there is no license attached to it. Feel free to use it in any way you see fit.
