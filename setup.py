from setuptools import setup, find_packages

setup(
    name="ark_biotech_dashboard",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "run-app=app.dashboard:main",
        ],
    },
)
