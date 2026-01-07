#!/usr/bin/env python
import os
import sys
from pathlib import Path


def _maybe_reexec_with_venv():
    if os.name != "nt":
        return
    venv_python = Path(__file__).resolve().parent / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        if Path(sys.executable).resolve() == venv_python.resolve():
            return
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    if sys.version_info >= (3, 14):
        raise RuntimeError(
            "Python 3.14 nao e suportado por este projeto. Use backend\\.venv\\Scripts\\python."
        )


def main():
    _maybe_reexec_with_venv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
