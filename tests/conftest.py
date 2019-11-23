
from pathlib import Path


def pytest_configure(config):
    # Create dummy manage.py file
    folder = Path.cwd()
    filepath = folder / 'manage.py'
    filepath.touch()


def pytest_unconfigure(config):
    # Delete manage.py file
    filepath = Path.cwd() / 'manage.py'
    filepath.unlink()
