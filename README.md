# BirdHouse – Backend

This repository contains the **backend service** for BirdHouse.

It is a small **FastAPI** application that stores device events (light status, alert switch, sightings) and optionally sends **Telegram notifications** when a sighting occurs.

The service exposes a simple REST API and is designed to run fully containerized using Docker.

---

## Requirements

The minimum requirements to run the project are:

- docker
- docker-compose

For convenience and simpler commands, it is also recommended to have:

- make

---

## Installation

Installing the project is straightforward if you have **Make** installed.

First, clone the repository and move into the project directory:

```bash
git clone https://github.com/<OWNER>/<REPO>.git
```
and once the repository has been cloned

```bash
cd BirdHouse
```

Then run:

```bash
docker-compose up -d
```

Or if you have make installed, you can simply run:

```bash
make
```

And that’s it — the backend will be running inside a Docker container.

Once started, the API will be available at:

```bash
http://localhost:8000
```

Swagger documentation:

```bash
http://localhost:8000/docs
```

## Configuration

Before running the project, you must create an environment file.

```bash
cp .env-dist .env
```

The most important variables to configure are:

- Database 
  - POSTGRES_HOST 
  - POSTGRES_USER 
  - POSTGRES_PASSWORD 
  - POSTGRES_DB

- Telegram
  - TELEGRAM_TOKEN
  - TELEGRAM_CHAT_ID

Other environment variables already have sensible defaults and usually do not need to be changed unless you want to customize behavior (cooldown time, camera URL, ports, etc.).

## Usage

The backend exposes a REST API under the /api prefix.

Main features:

- Store light on/off events 
- Enable or disable alert notifications 
- Send Telegram messages or photos when a sighting occurs (if alerts are enabled)

You can interact with the API either via HTTP requests or directly from the Swagger UI.

## Tests

Tests are written using unittest and can be executed inside the running container:

```bash
docker-compose exec birdhouse pytest
```

Or if you have make installed, you can simply run:

```bash
make test
```

## Have fun

Enjoy using BirdHouse and feel free to adapt it to your own setup and ideas.