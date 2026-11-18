"""Verify that destructive tests cannot remove the user's dataset cache."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def test_parallel_repositories_preserve_user_cache(tmp_path: Path) -> None:
    """Run real community removal in two workers with a protected user cache."""
    project = tmp_path / "project"
    project.mkdir()
    shutil.copyfile(Path(__file__).parents[2] / "conftest.py", project / "conftest.py")
    home = tmp_path / "home"
    cache = home / ".colour-science" / "colour-datasets"
    cache.mkdir(parents=True)
    marker = cache / "user-data.txt"
    marker.write_text("Keep the user cache intact.\n")
    test = """import os
from pathlib import Path
from colour_datasets import Community, Configuration

def test_remove():
    configuration = Configuration()
    Path(__file__).with_suffix('.repository').write_text(configuration.repository)
    community = Community(
        {'community': {}, 'records': {'hits': {'hits': []}}}, configuration
    )
    community.remove()
    assert not Path(configuration.repository).exists()
"""
    for name in ("test_first.py", "test_second.py"):
        (project / name).write_text(test)
    environment = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    environment.pop("COLOUR_SCIENCE__COLOUR_DATASETS__REPOSITORY", None)
    environment.pop("PYTEST_ADDOPTS", None)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "pytest",
            "-n",
            "2",
            "--dist=loadfile",
            "-o",
            "addopts=",
        ],
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    repositories = {path.read_text() for path in project.glob("test_*.repository")}
    assert len(repositories) == 2
    assert str(cache) not in repositories
    assert marker.read_text() == "Keep the user cache intact.\n"
