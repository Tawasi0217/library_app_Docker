# Docker Swarm Deployment

This app is packaged with a Miniconda-based Docker image.

## Build Image

```powershell
docker build -t library-loan-app:latest .
```

If you deploy to a remote Swarm cluster, push the image to a registry and update
`docker-stack.yml` to use that registry image.

## Deploy To Docker Swarm

```powershell
docker swarm init
docker stack deploy -c docker-stack.yml library
```

Open:

```text
http://127.0.0.1:5000/books
```

The container runs `python init_db.py` on startup, so SQLite tables and seed data
are created automatically. The SQLite database is stored in the named volume
`library_data`.

## Notes

- `docker-stack.yml` uses `replicas: 1` because SQLite should not be written by
  multiple replicated app containers at the same time.
- Change `SECRET_KEY` before production use.
- For local non-Swarm testing, run `docker compose up --build`.
