# Library App Docker

Flask + SQLAlchemy library loan app packaged for Docker Swarm.

## Build

```powershell
docker build -t library-loan-app:latest .
```

## Deploy With Docker Swarm

```powershell
docker swarm init
docker stack deploy -c docker-stack.yml library
```

Open:

```text
http://127.0.0.1:5000/books
```

The container initializes the SQLite database on startup by running
`python init_db.py`. SQLite data is stored in the `library_data` named volume.

For local testing without Swarm:

```powershell
docker compose up --build
```
