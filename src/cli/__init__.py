"""
src/cli: Command-Line Interface package for HelixCore.
"""

__all__ = ["cli_entrypoint"]


def cli_entrypoint():
    from .main import cli_entrypoint as _entry
    return _entry()
