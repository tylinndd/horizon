"""
Generate initial Alembic migration
Run this after creating models to generate the first migration
"""
import subprocess
import sys

if __name__ == "__main__":
    # Generate migration
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", "Initial migration"],
        cwd="."
    )
    sys.exit(result.returncode)

