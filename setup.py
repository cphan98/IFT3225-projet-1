from setuptools import setup

setup(
    name="tp1",
    version="0.1",
    py_modules=["extract", "genere"],
    entry_points={
        "console_scripts": [
            "extract=extract:main",
            "genere=genere:main",
        ],
    },
)
