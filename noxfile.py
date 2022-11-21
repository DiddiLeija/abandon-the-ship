import nox

file_list = ("main.py", "noxfile.py")


@nox.session
def format(session):
    "Run formatters, to keep the order."
    # Install requirements
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-lint.txt")
    # Run formatters
    session.run("isort", *file_list)
    session.run("black", *file_list)


@nox.session
def lint(session):
    "Run linters to see if everything's civilized."
    # Install requirements
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-lint.txt")
    # Run linters
    session.run("flake8", *file_list, "--max-line-length=127", "--ignore=F841")
    session.run("isort", "--check-only", *file_list)
    session.run("black", "--check", *file_list)
