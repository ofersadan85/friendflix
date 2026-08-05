build tag="test":
  docker build -t friendflix-backend:{{tag}} .

run tag="test":
  docker run --rm -it --env-file .env -p 8000:8000 friendflix-backend:{{tag}}

dev:
  uv run fastapi dev

postgres:
  docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 127.0.0.1:5432:5432 postgres:17-alpine

reset:
  - docker stop postgres
  - docker rm postgres
  just postgres
  just dev
