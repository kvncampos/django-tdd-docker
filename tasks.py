import os
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv
from invoke import task

# LOGIN TO HEROKU BEFORE STARTING ANY HEROKU TASKS

# Load environment variables from .env file
load_dotenv()

# Fetch HEROKU_APP_NAME from environment
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

COMPOSE_FILE = Path("development") / "docker-compose.yml"
CONTAINER_NAME = "development-movies-1"


# ----------------------------------------------------------------------
# HEROKU TASKS
# ----------------------------------------------------------------------
@task
def heroku_cli(c):
    """Login to Heroku APP CLI Using Bash."""
    command = f"heroku run bash --app {HEROKU_APP_NAME}"
    c.run(command)


import os
import re

from dotenv import load_dotenv
from invoke import task

# Load environment variables from .env file
load_dotenv()

# Fetch HEROKU_APP_NAME from environment
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")


def wait_for_postgres_creation(c, addon_name):
    """Wait for PostgreSQL add-on to be fully created"""
    max_attempts = 10
    attempt = 0
    delay = 30  # seconds between checks

    while attempt < max_attempts:
        attempt += 1
        print(
            f"Checking PostgreSQL {addon_name} creation status... (Attempt {attempt}/{max_attempts})",
        )

        # Check the add-on status using heroku addons:info
        pg_info_output = c.run(
            f"heroku addons:info {addon_name} --app {HEROKU_APP_NAME}",
            hide=True,
        ).stdout.strip()

        # Look for the state in the output after stripping whitespace
        if "created" in pg_info_output:
            print("PostgreSQL has been created and is ready.")
            break
        print("PostgreSQL is still being created. Waiting...")

        time.sleep(delay)

    if attempt == max_attempts:
        raise RuntimeError(
            f"PostgreSQL add-on {addon_name} was not created after {max_attempts} attempts.",
        )


def wait_for_heroku_ready(c):
    """Wait until the Heroku app and web dyno are ready"""
    max_attempts = 10
    attempt = 0
    delay = 10  # seconds between checks

    while attempt < max_attempts:
        attempt += 1
        print(
            f"Checking if Heroku app and PostgreSQL are ready... (Attempt {attempt}/{max_attempts})",
        )

        # Check if web dyno is up
        ps_output = c.run(f"heroku ps --app {HEROKU_APP_NAME}", hide=True).stdout
        if "web.1: up" in ps_output:
            print("Web dyno is up.")
            break
        print("Web dyno is not up yet. Waiting...")

        time.sleep(delay)

    if attempt == max_attempts:
        raise RuntimeError(
            "Failed to detect that Heroku app and web dyno are ready after multiple attempts.",
        )


@task
def heroku_up(c):
    """Scale up Heroku dyno, add PostgreSQL, run migrations, and load data"""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    print(f"Scaling up Heroku dyno and setting up the app for: {HEROKU_APP_NAME}...")

    # Scale the web dyno up
    c.run(f"heroku ps:scale web=1 --app {HEROKU_APP_NAME}")

    # Check if PostgreSQL add-on already exists
    addons_list_output = c.run(
        f"heroku addons --app {HEROKU_APP_NAME}",
        hide=True,
    ).stdout

    # Look for any PostgreSQL add-on in the output
    if "heroku-postgresql" in addons_list_output:
        print("PostgreSQL add-on already exists for this app. Skipping creation.")

    else:
        # Add PostgreSQL add-on (essential-0 plan)
        print("No PostgreSQL add-on found. Creating a new PostgreSQL add-on...")
        result = c.run(
            f"heroku addons:create heroku-postgresql:essential-0 --app {HEROKU_APP_NAME}",
        )

        # Extract the PostgreSQL add-on name from the result
        match = re.search(r"postgresql-\S+", result.stdout)
        if match:
            addon_name = match.group(0)
            print(f"PostgreSQL add-on {addon_name} is being created...")

            # Wait for PostgreSQL add-on to be fully created
            wait_for_postgres_creation(c, addon_name)
        else:
            raise RuntimeError("Failed to detect the PostgreSQL add-on name.")

    # Wait for the web dyno to be fully up
    wait_for_heroku_ready(c)

    # Run database migrations
    c.run(f"heroku run python manage.py migrate --app {HEROKU_APP_NAME}")

    # Load initial data from movies.json
    c.run(f"heroku run python manage.py loaddata movies.json --app {HEROKU_APP_NAME}")

    print(f"Heroku app {HEROKU_APP_NAME} is up and running.")


@task
def heroku_down(c):
    """Scale down the Heroku dyno to stop the app"""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    print(f"Scaling down Heroku dyno for app: {HEROKU_APP_NAME}...")

    # Scale the web dyno down (stop it)
    c.run(f"heroku ps:scale web=0 --app {HEROKU_APP_NAME}")

    print(f"Heroku app {HEROKU_APP_NAME} is scaled down.")


@task
def heroku_shell(c):
    """Open a shell in the running Heroku dyno for the specified app."""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    print(f"Opening a shell in the Heroku dyno for app: {HEROKU_APP_NAME}...")

    # Run the Heroku command to open a shell (bash) in a running dyno
    c.run(f"heroku run bash --app {HEROKU_APP_NAME}", pty=True)

    print(f"Shell session started for app: {HEROKU_APP_NAME}.")


@task
def heroku_destroy(c):
    """Scale up the Heroku dyno, then destroy PostgreSQL add-on"""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    print(
        f"Scaling down the Heroku dyno to prepare for PostgreSQL destruction for: {HEROKU_APP_NAME}...",
    )

    # Scale the web dyno down
    c.run(f"heroku ps:scale web=0 --app {HEROKU_APP_NAME}")

    # Try to destroy the PostgreSQL add-on
    print(
        f"Attempting to destroy the Heroku PostgreSQL add-on for app: {HEROKU_APP_NAME}...",
    )

    try:
        # Run the command, but capture both stdout and stderr
        result = c.run(
            f"heroku addons:destroy heroku-postgresql --app {HEROKU_APP_NAME} --confirm {HEROKU_APP_NAME}",
            warn=True,
            hide=True,
        )

        # Combine stdout and stderr to check for "not_found"
        combined_output = result.stdout + result.stderr

        if "Error ID: not_found" in combined_output:
            print(
                f"PostgreSQL add-on for {HEROKU_APP_NAME} has already been destroyed or does not exist.",
            )
        else:
            print(f"Heroku PostgreSQL add-on destroyed for app {HEROKU_APP_NAME}.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


@task
def export_requirements(c):
    """Export requirements.txt from poetry.lock and place it inside the ./app directory"""
    # Check if poetry is installed
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            check=True,
            stdout=subprocess.PIPE,
        )
        print(result.stdout.decode("utf-8"))
    except subprocess.CalledProcessError:
        print("Poetry is not installed. Please install Poetry first.")
        return

    # Define paths using Path from pathlib
    project_root = Path(__file__).parent
    app_dir = project_root / "app"
    requirements_file = app_dir / "requirements.txt"

    # Create the app directory if it doesn't exist
    app_dir.mkdir(exist_ok=True)

    # Generate requirements.txt from poetry.lock
    print("Exporting requirements.txt from poetry.lock...")
    c.run(
        f"poetry export -f requirements.txt --output {requirements_file} --without-hashes",
    )

    # Verify that the requirements.txt file was created
    if requirements_file.exists():
        print(f"requirements.txt successfully created at {requirements_file}")
    else:
        print("Failed to create requirements.txt.")


@task
def build_and_release_heroku(c):
    """Build, Push and Release Heroku App."""

    def _build_heroku(c):
        """Build the Heroku Docker image"""
        print("Building Heroku Docker image...")
        c.run(
            f"docker buildx build --platform linux/amd64 -f development/Dockerfile.prod -t registry.heroku.com/{HEROKU_APP_NAME}/web .",
        )
        print("Heroku Docker image built successfully.")

    def _push_heroku(c):
        print("Pushing Image to Registry...")
        command = f"docker push registry.heroku.com/{HEROKU_APP_NAME}/web:latest"
        c.run(command)
        print("Image Pushed Successfully.")

    def _release_heroku(c):
        command = f"heroku container:release web --app {HEROKU_APP_NAME}"
        c.run(command)

    _build_heroku(c)
    _push_heroku(c)
    _release_heroku(c)


@task
def run_local_heroku(c):
    """Run the Heroku Docker container with additional environment variables"""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set in the environment.")
        return

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        print("Error: SECRET_KEY is not set in the environment.")
        return

    print(f"Running Heroku Docker container for app: {HEROKU_APP_NAME}...")

    # Build the docker run command with the required options
    command = (
        f"docker run --platform linux/amd64 --name django-tdd "  # Added a space at the end
        f"-e 'PORT=8765' "  # Added a space at the end
        f"-e 'DATABASE_URL={DATABASE_URL}' "  # Added a space at the end
        f"-e 'SECRET_KEY={SECRET_KEY}' "  # Added a space at the end
        f"-p 8008:8765 "  # Added a space at the end
        f"registry.heroku.com/{HEROKU_APP_NAME}/web:latest"  # This line remains unchanged
    )

    # Execute the command
    c.run(command)

    print(
        f"Heroku Docker container '{HEROKU_APP_NAME}' is running on port 8008 (bound to container port 8765).",
    )


@task
def stop_local_heroku(c):
    """Stop the Heroku Docker container"""
    print("Bringing Down Container django-tdd...")
    command = "docker stop django-tdd"
    c.run(command)
    print("Container Successfully Stopped.")


# ----------------------------------------------------------------------
# LOCAL TASKS
# ----------------------------------------------------------------------


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


# --------------------------------------------------
# TESTS
# --------------------------------------------------
@task(
    help={
        "keyword": "Keyword expression to filter tests. If provided, it uses pytest's '-k' option. Defaults to None, which runs all tests.",
        "warnings": "If True, warnings will be enabled. Defaults to False, which disables warnings.",
        "coverage": "If True, coverage will be run using pytest-cov. Defaults to False, which just runs the tests.",
        "coverage_report": "If True, creates coverage in html format.",
    },
)
def run_tests(ctx, keyword=None, warnings=False, coverage=False, coverage_report=False):
    """Run Pytests, with optional coverage reporting.

    This task allows you to run Pytests inside a Docker container, with options to enable coverage
    reporting and filter tests using keyword expressions. By default, it disables warnings unless
    warnings=True is passed.

    Parameters
    ----------
        - ctx : The context object passed by invoke.
        - keyword (str, optional) : Keyword expression to filter tests. If provided, it uses pytest's '-k' option.
                                    Defaults to None, which runs all tests.
        - warnings (bool, optional) : If True, warnings will be enabled. Defaults to False, which disables warnings.
        - coverage (bool, optional) : If True, coverage will be run using pytest-cov. Defaults to False, which just runs the tests.

    """
    # Construct the base pytest command
    command = f"docker exec -it {CONTAINER_NAME} pytest"

    # Add coverage flag if coverage=True
    if coverage:
        command += " --cov=."

    # Create HTML Coverage
    if coverage_report:
        command += " --cov=. --cov-report html"

    # Append the keyword expression if provided
    if keyword:
        command += f" -k '{keyword}'"

    # Disable warnings if warnings=False
    if not warnings:
        command += " -p no:warnings"

    # Run the command
    ctx.run(command, pty=True)


@task
def open_coverage_report(ctx):
    command = "open app/htmlcov/index.html"
    ctx.run(command)


@task(
    help={
        "path": "The directory or file to check. Defaults to the current directory ('.').",
        "auto_format": "If True, Ruff will attempt to fix issues automatically. Defaults to False.",
        "config_file": "Path to a Ruff configuration file (e.g., pyproject.toml). Defaults to None.",
        "select": "Comma-separated error codes to select specific linting rules. Defaults to None (checks all rules).",
        "ignore": "Comma-separated error codes to ignore specific linting rules. Defaults to None (does not ignore any).",
        "verbose": "If True, Ruff will run in verbose mode. Defaults to False.",
        "statistics": "If True, Ruff will output statistics about linting issues. Defaults to False.",
        "exit_on_failure": "If True, the task will stop execution if any linting issues are found. Defaults to False.",
    },
)
def heroku_ruff(
    ctx,
    path=".",
    auto_format=False,
    config_file=None,
    select=None,
    ignore=None,
    verbose=False,
    statistics=False,
    exit_on_failure=False,
):
    """Run Ruff linter on the specified path, optionally fixing issues and applying additional configurations.

    This task runs Ruff inside the specified Heroku app.
    """
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    # Base Ruff command
    command = f"ruff check {path} --exclude 'tests/*'"

    # Add options
    if auto_format:
        command += " --fix"

    if config_file:
        command += f" --config {config_file}"

    if select:
        command += f" --select {select}"

    if ignore:
        command += f" --ignore {ignore}"

    if verbose:
        command += " --verbose"

    if statistics:
        command += " --statistics"

    if exit_on_failure:
        command += " --exit-zero"

    # Run the command inside Heroku container
    ctx.run(f"heroku run '{command}' --app {HEROKU_APP_NAME}", pty=True)


@task
def heroku_format_code(c):
    """Run Black for formatting and Ruff for linting/fixing inside the Heroku container."""
    if not HEROKU_APP_NAME:
        print("Error: HEROKU_APP_NAME is not set in the environment.")
        return

    # Run Black in Heroku container
    print("Running Black in Heroku container...")
    c.run(f"heroku run 'black .' --app {HEROKU_APP_NAME}", pty=True)

    # Run Ruff in Heroku container
    print("Running Ruff in Heroku container...")
    c.run(f"heroku run 'ruff check . --fix' --app {HEROKU_APP_NAME}", pty=True)


@task
def local_ruff(c, path=".", auto_format=False):
    """Run Ruff linter on the local environment, excluding specific directories.

    Parameters
    ----------
        - c : The context object passed by invoke.
        - path (str, optional) : The directory or file to check. Defaults to current directory.
        - auto_format (bool, optional) : If True, Ruff will attempt to fix issues automatically. Defaults to False.

    """
    # Base Ruff command for local environment
    command = f"ruff check {path} --exclude './app/tests/*' --exclude './app/movies/migrations/*' --exclude 'tasks.py'"

    # Add auto-format option if required
    if auto_format:
        command += " --fix"

    # Run the command
    c.run(command, pty=True)


@task
def local_format_code(c):
    """Run Black for formatting and Ruff for linting/fixing."""
    print("Running Black...")
    c.run("black .")
    print("Running Ruff...")
    c.run("ruff check . --fix")


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
        f"docker exec -it {CONTAINER_NAME} python manage.py makemigrations",
        pty=True,
    )


@task
def migrate(ctx):
    """Run 'python manage.py migrate' inside the Docker container."""
    ctx.run(f"docker exec -it {CONTAINER_NAME} python manage.py migrate", pty=True)


@task
def checks(ctx):
    """Open a shell in the Docker container 'development-movies-1'."""
    ctx.run("pre-commit run --all-files", pty=True)
