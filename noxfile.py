import nox

import os
import shutil
from pathlib import Path
import platform
import sys
nox.options.error_on_external_run = True
nox.options.sessions =['lock', 'tests']


@nox.session
def build(session):
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    session.run('uv', 'build')
    # uv publish コマンドを実行
    session.run(
        "uv",
        "publish",
        "--publish-url",
        "https://test.pypi.org/legacy/",
        "--token",
        os.environ["TEST_PYPI_TOKEN"],
    )

def constraints(session):
    filename = f'python-{session.python}-{sys.platform}-{platform.machine()}.txt'

    return Path('constraints') / filename

@nox.session(python=['3.8', '3.9', '3.10', '3.11', '3.12'], venv_backend='uv')
def lock(session):
    filename = constraints(session)
    filename.parent.mkdir(exist_ok=True)
    session.run('uv', 'pip', 'compile', 'pyproject.toml',
                '--upgrade', '--quiet', '--all-extras',
                f'--output-file={filename}')



def install_coverage_pth(session):
    output = session.run(
        "python", "-c",
        "import sysconfig; print(sysconfig.get_path('purelib'))",
        silent=True,
    )
    purelib = Path(output.strip())

    (purelib/'coverage.pth').write_text("import coverage; coverage.process_startup()")


@nox.session(python=['3.8', '3.9', '3.10', '3.11', '3.12'], venv_backend='uv')
def tests(session):

    constraints_file = constraints(session)

    # 制約ファイルを使って依存関係をインストール
    session.install("-r", str(constraints_file), ".", "pytest", "coverage[toml]")
    install_coverage_pth(session)

    try:
        args = ['coverage', 'run', '-m', 'pytest', *session.posargs]
        session.run(*args, env={"COVERAGE_PROCESS_START": "pyproject.toml"})

    finally:
        session.notify('coverage')

@nox.session(python=['3.8', '3.9', '3.10', '3.11', '3.12'], venv_backend='uv')
def coverage(session):
    session.install("-c", constraints(session), 'coverage[toml]')
    if any(Path().glob('.coverage.*')):
        session.run('coverage', 'combine')

    session.run('coverage', 'report')
