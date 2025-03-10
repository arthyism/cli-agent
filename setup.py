from setuptools import setup, find_packages

setup(
    name="cli-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "groq",
        "instructor",
        "pydantic",
        "dotenv",
        "eval_type_backport"
    ],
    entry_points={
        "console_scripts": [
            "cli-agent=cli_agent.main:run",
        ],
    },
)
