# FriendFlix

This is a demo project for watching and sharing movies and TV episodes with friends.

## Usage

To run the project locally, (with docker desktop installed) follow these steps:

```bash
git clone https://github.com/ofersadan85/friendflix
cd friendflix
cp example.env .env  # copy the example.env file to .env
# edit the .env file and set the values for the environment variables as needed
docker compose up --build --detach
```

Follow the other instructions in this README.md file for setting up the project for development or for running the project without Docker.

### Backend API Server (Flask)

Build the backend dependencies. Make sure to run the following commands in the `backend` directory (and it's recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

> [!WARNING]
> Change the value of the `FLASK_SECRET_KEY` in the [backend/.env](backend/.env) file to a random string. This is used to secure the session cookies / JWT tokens.

This project must have a valid API key for TMDB. Copy the file [backend/example.env](backend/example.env) to `backend/.env` and replace the placeholder for `TMDB_API_KEY` with a valid API key.

> [!CAUTION]
> The API key should be kept secret. Do not share it publicly.

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

> [!NOTE]
> `requirements.txt` and `requirements-dev.txt` are generated using [poetry](https://python-poetry.org/) which is a more advanced package manager for Python. If you want to use poetry, you can install the dependencies using `poetry install` and run the tests using `poetry run pytest`.

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

The app will also create the first admin username for you automatically, see the terminal output for the username and password.

If you would like to set your own values for the first admin user, you can do so by setting the `FLASK_INITIAL_ADMIN_USERNAME`, `FLASK_INITIAL_ADMIN_EMAIL`, and `FLASK_INITIAL_ADMIN_PASSWORD` environment variables. See the [backend/example.env](backend/example.env) file for an example.

> [!WARNING]
> The initial admin user is created only once, when the database file is created. If you delete the database file, the initial admin user will be created again. It is also highly recommended to change the initial admin password after the first login, even if you set your own password in the environment variables.

## Running the Project with Docker

This project can also be run using Docker.
This is useful if you don't want to install the dependencies on your machine, or if you want to run the project in a containerized environment.

> [!NOTE]
> The following commands will build and run the project in ***production mode***.

To run the backend (from the backend directory):

```bash
docker build -t friendflix-backend .
docker run -p 8080:8080 friendflix-backend
```

To run the frontend (from the frontend directory):

```bash
npm run build
docker build -t friendflix-frontend .
docker run -p 8081:80 friendflix-frontend
```

The backend will be running at [http://localhost:8080](http://localhost:8080) and the frontend will be running at [http://localhost:8081](http://localhost:8081).

If you want to see what each Dockerfile does, you can check the [backend/Dockerfile](backend/Dockerfile) and [frontend/Dockerfile](frontend/Dockerfile) files.

## Docker Compose

You can also run the project using Docker Compose. This is useful if you want to run the project in a containerized environment, but you don't want to build and run each container separately.

To run the project using Docker Compose:

1. `git clone` this repository and `cd` into the project directory.
2. Copy the [example.env](example.env) file to `.env` and set the values for the environment variables as needed.
3. Run the following command:

```bash
docker compose up --build --detach
```

Which will both build and all that is needed in the background. It will also create a new `./data/db.sqlite` file for the database at your local machine, so you can persist the data between container restarts.

Without the `--detach` flag, you will see the logs of the containers in the terminal, and you can stop them by pressing Ctrl+C. With the `--detach` flag (also available as `-d`), the containers will run in the background (which is useful for production environments) and you can stop them using `docker compose down` from the within the project directory.

## VsCode shortcuts

This project has some shortcuts for VsCode that can be used to run the tests and the development servers, for easier development. You can find them in [.vscode/tasks.json](.vscode/tasks.json). Run Ctrl+Shift+P and type "Tasks: Run Task" to see the available tasks. For example, running the "DEV Server" task will start the frontend development server and the backend server on a split terminal.

## CI/CD

[![Frontend Tests](https://github.com/ofersadan85/friendflix/actions/workflows/react_tests.yml/badge.svg)](https://github.com/ofersadan85/friendflix/actions/workflows/react_tests.yml)
[![Backend Tests](https://github.com/ofersadan85/friendflix/actions/workflows/python_tests.yml/badge.svg)](https://github.com/ofersadan85/friendflix/actions/workflows/python_tests.yml)

This project uses GitHub Actions for CI/CD. The workflow files can be found in the [.github/workflows](.github/workflows) directory. Both the frontend tests and the backend tests are run on every push to the `main` branch and on every pull request to the `main` branch, but both only run on changes to their respective directories.

CD (Continuous Deployment to a production server) is not set up yet. [//]: # (TODO)

## License

This project is free and open source, see the [LICENSE](LICENSE) file for more information.
