import os

from invoke import task

COMPOSE_FILE = os.path.join("development", "docker-compose.yml")
CONTAINER_NAME = "development-movies-1"


@task
def down(ctx, volumes=False):
    """Stop and remove Docker containers, with optional volume removal."""
    command = f"docker-compose -f {COMPOSE_FILE} down"
    if volumes:
        command += " -v"
    ctx.run(command, pty=True)


@task
def start(ctx):
    """Start Docker containers in detached mode."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} up -d", pty=True)


@task
def debug(ctx):
    """Start Docker containers in attached mode with rebuild."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} up --build", pty=True)


@task
def stop(ctx):
    """Stop running Docker containers."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} stop", pty=True)


@task
def restart(ctx):
    """Restart Docker containers."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} restart", pty=True)


@task
def logs(ctx, follow=False):
    """Show Docker container logs, with optional following."""
    command = f"docker-compose -f {COMPOSE_FILE} logs"
    if follow:
        command += " -f"
    ctx.run(command, pty=True)


@task
def build(ctx, no_cache=False):
    """Build Docker images."""
    command = f"docker-compose -f {COMPOSE_FILE} build"
    if no_cache:
        command += " --no-cache"
    ctx.run(command, pty=True)


@task
def build_no_cache(ctx):
    """Build Docker images without using cache."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} build --no-cache", pty=True)


@task
def remove_volumes(ctx):
    """Remove all Docker volumes."""
    ctx.run("docker volume prune -f", pty=True)


@task
def destroy(ctx):
    """Stop and remove Docker containers, and remove all associated volumes."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} down -v", pty=True)
    ctx.run("docker volume prune -f", pty=True)


@task
def pytest(ctx, keyword=None):
    """
    Run Pytests.

    Parameters:
        - ctx : The context object passed by invoke.
        - keyword (str, optional) : Keyword expression to filter tests. If provided, it uses pytest's '-k' option. Defaults to None, which runs all tests.
    """
    # Construct the base pytest command
    command = f"docker exec -it {CONTAINER_NAME} pytest"

    # Append the keyword expression if provided
    if keyword:
        command += f" -k '{keyword}'"

    # Run the command
    ctx.run(command, pty=True)


@task
def ruff(ctx, fix=False):
    """Run Ruff linter recursively on all files in the current directory, optionally fixing issues."""
    command = "ruff check ." if not fix else "ruff check --fix ."
    ctx.run(f"docker exec -it {CONTAINER_NAME} {command}", pty=True)


@task
def create_superuser(ctx, fix=False):
    """Run Ruff linter recursively on all files in the current directory, optionally fixing issues."""
    command = "python manage.py createsuperuser"
    ctx.run(f"docker exec -it {CONTAINER_NAME} {command}", pty=True)


@task
def cli(ctx, shell="/bin/bash"):
    """Open a shell in the Docker container 'development-movies-1'."""
    ctx.run(f"docker exec -it {CONTAINER_NAME} {shell}", pty=True)


@task
def makemigrations(ctx):
    """Run 'python manage.py makemigrations' inside the Docker container."""
    ctx.run(
        f"docker exec -it {CONTAINER_NAME} python manage.py makemigrations", pty=True
    )


@task
def migrate(ctx):
    """Run 'python manage.py migrate' inside the Docker container."""
    ctx.run(f"docker exec -it {CONTAINER_NAME} python manage.py migrate", pty=True)


@task
def checks(ctx):
    """Open a shell in the Docker container 'development-movies-1'."""
    ctx.run("pre-commit run --all-files", pty=True)
