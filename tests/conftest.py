"""Shared pytest fixtures. Auto-discovered by pytest."""

import pytest


@pytest.fixture
def sample_fixture():
    """Example fixture - customize for your project"""
    # Setup
    data = {"key": "value"}
    yield data
    # Teardown (if needed)
