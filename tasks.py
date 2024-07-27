from invoke import task
import os

COMPOSE_FILE = os.path.join("development", "docker-compose.yml")


@task
def down(ctx, volumes=False):
    """Stop and remove Docker containers, with optional volume removal."""
    command = f"docker-compose -f {COMPOSE_FILE} down"
    if volumes:
        command += " -v"
    ctx.run(command, pty=True)


@task
def up_detached(ctx):
    """Start Docker containers in detached mode."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} up -d", pty=True)


@task
def debug(ctx):
    """Start Docker containers in attached mode."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} up", pty=True)


@task
def start(ctx):
    """Start existing Docker containers."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} start", pty=True)


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
def remove_volumes(ctx):
    """Remove all Docker volumes."""
    ctx.run("docker volume prune -f", pty=True)


@task
def destroy(ctx):
    """Stop and remove Docker containers, and remove all associated volumes."""
    ctx.run(f"docker-compose -f {COMPOSE_FILE} down -v", pty=True)
    ctx.run("docker volume prune -f", pty=True)
