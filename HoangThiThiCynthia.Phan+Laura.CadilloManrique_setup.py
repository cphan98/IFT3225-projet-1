from setuptools import setup

setup(
    name="tp1",
    version="0.1",
    py_modules=["HoangThiThiCynthia.Phan+Laura.CadilloManrique_extract", "HoangThiThiCynthia.Phan+Laura.CadilloManrique_genere"],
    entry_points={
        "console_scripts": [
            "extract=HoangThiThiCynthia.Phan+Laura.CadilloManrique_extract:main",
            "genere=HoangThiThiCynthia.Phan+Laura.CadilloManrique_genere:main",
        ],
    },
)
