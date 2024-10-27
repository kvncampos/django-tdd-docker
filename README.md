<div align="center" id="top">
  <img src="./.github/app.gif" alt="Django TDD Project" />
</div>

<h1 align="center">Django TDD Project</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/kvncampos/django-tdd-docker?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/kvncampos/django-tdd-docker?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/kvncampos/django-tdd-docker?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/kvncampos/django-tdd-docker?color=56BEB8">
</p>

## Table of Contents

- [About](#dart-about)
- [Technologies](#rocket-technologies)
- [Requirements](#white_check_mark-requirements)
- [Starting](#checkered_flag-starting)
- [License](#memo-license)
- [Author](#heart-author)

## :dart: About ##

This project demonstrates Test-Driven Development (TDD) using Django and Django REST Framework, with containerization through Docker. It is designed to run in local development and can be deployed to Heroku for production.

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)
- [Heroku](https://www.heroku.com/)

## :white_check_mark: Requirements ##

Before starting, make sure you have the following installed:

- [Git](https://git-scm.com)
- [Python 3.12](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/kvncampos/django-tdd-docker

# Access
$ cd django-tdd-docker

# Install dependencies
$ poetry shell
$ poetry install

# Local Development, Run Project
$ invoke run

# The server will initialize at <http://localhost:8009/>

# HTTP STATUS
$ http://localhost:8009/ping/

> Response:
    {
      "ping": "pong!"
    }

# Using Docker
$ docker-compose -f development/docker-compose.yml up --build

# The server will initialize at <http://localhost:8000/>
