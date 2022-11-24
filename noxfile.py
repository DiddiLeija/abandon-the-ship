import os
import sys

import nox

nox.options.sessions = ["format", "lint"]

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


@nox.session
def package(session):
    "Build and package everything up."
    # First of all, install the requirements
    session.install("-r", "requirements.txt")
    # Look for the 'dist' path, that will store everything
    session.warn("Looking for the destination path...")
    dist_generation = "import os; os.mkdir('./dist')"
    if os.path.exists("./dist"):
        if not input(
            "The destination directory ('./dist') already exists. Do you want to remove it? (y/n) "
        ).strip().lower() in ("y", "yes"):
            session.warn("Aborting...")
            quit()
        dist_generation = (
            "import os, shutil; shutil.rmtree('./dist'); os.mkdir('./dist')"
        )
    session.run("python", "-c", dist_generation)
    # Zip the source code
    session.warn("Generating the source code distribution...")
    session.run(
        "python",
        "-c",
        "import os, shutil; shutil.copy('main.py', './dist/main.py'); "
        "shutil.copy('resource.pyxres', './dist/resource.pyxres')",
    )
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        "./dist/source.zip",
        "./dist/main.py",
        "./dist/resource.pyxres",
    )
    # Generate and zip the Pyxel executable
    session.warn("Generating the Pyxel executable...")
    session.cd("dist")
    session.run("pyxel", "package", ".", "main.py")
    session.cd("..")
    session.run(
        "python",
        "-c",
        "import os; os.rename('./dist/dist.pyxapp', './dist/pyxel_dist.pyxapp')",
    )
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        "./dist/pyxel_dist.zip",
        "./dist/pyxel_dist.pyxapp",
    )
    # If Windows, create the cx_Freeze executable
    if sys.platform == "win32":
        session.warn("Running in Windows, generating the cx_Freeze executable...")
        session.install("cx_Freeze")
        session.run("python", "setup.py", "build")
        session.run(
            "python",
            "-c",
            "import os, shutil; exe_path = os.listdir('./build')[0]; "
            "shutil.copy2('resource.pyxres', f'./build/{exe_path}/resource.pyxres')",
        )
        session.run("python", "-m", "zipfile", "-c", "./dist/windows.zip", "./build")
    else:
        # It's polite to notify when a step is ignored... well, that's what I think.
        session.warn(
            "Not running in Windows, ignoring the cx_Freeze executable build..."
        )
    # Before closing, it's cleanup time!
    session.warn("Cleaning up the excedents...")
    session.run(
        "python",
        "-c",
        "import os; os.remove('./dist/main.py'); os.remove('./dist/resource.pyxres'); "
        "os.remove('./dist/pyxel_dist.pyxapp')",
    )
    if os.path.exists("./build"):
        session.run("python", "-c", "import shutil; shutil.rmtree('./build')")
    # Send a success message
    session.warn("All done! The contents are ready at './dist'.")
