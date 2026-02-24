#!/bin/bash
# =============================================================================
# Section 9 — Docker: Beginner Exercises (B1-B8)
# Guide: docs/curriculum/09-docker-containerization.md
# =============================================================================

# Exercise 5.B.1 — Pull & Run
# TODO: docker pull python:3.11-slim
# TODO: docker run --rm python:3.11-slim python -c "print('Hello from Docker')"

# Exercise 5.B.2 — List containers, images, interact
# TODO: docker ps -a
# TODO: docker images
# TODO: docker run -it python:3.11-slim bash

# Exercise 5.B.3 — Port mapping
# TODO: docker run -p 8080:80 nginx
# TODO: curl http://localhost:8080

# Exercise 5.B.4 — Environment variables
# TODO: docker run -e MY_VAR=hello python:3.11-slim python -c "import os; print(os.environ['MY_VAR'])"

# Exercise 5.B.5 — Volume mount
# TODO: docker run -v $PWD:/app -w /app python:3.11-slim python script.py

# Exercise 5.B.6 — Build first image
# TODO: Write a Dockerfile (see B06_Dockerfile)
# TODO: docker build -t my-first-image .
# TODO: docker run my-first-image

# Exercise 5.B.7 — Container logs
# TODO: docker logs <container_id>
# TODO: docker logs -f <container_id>

# Exercise 5.B.8 — Container lifecycle
# TODO: docker run -d --name myapp nginx
# TODO: docker stop myapp
# TODO: docker start myapp
# TODO: docker rm myapp
