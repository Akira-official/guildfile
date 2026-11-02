"""
tests/test_blueprint_parser.py
Unit tests for blueprint schema validation.
"""

import os
import pytest
from src.core.blueprint_parser import load_blueprint, BlueprintSchema


def test_load_valid_blueprint():
    sample_path = os.path.join(os.path.dirname(__file__), "..", "templates", "dev-startup.yaml")
    blueprint = load_blueprint(sample_path)
    assert isinstance(blueprint, BlueprintSchema)
    assert blueprint.metadata.name == "DevHub Community"
    assert len(blueprint.roles) > 0
    assert len(blueprint.categories) > 0


def test_missing_blueprint_raises_error():
    with pytest.raises(FileNotFoundError):
        load_blueprint("non_existent_file.yaml")

