from setuptools import setup, find_packages

version = {}
with open("overhang/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="overhang",
    version=version["__version__"],
    author="Peter Vegh",
    description="Compendium of overhangs",
    long_description=open("pypi-readme.rst").read(),
    long_description_content_type="text/x-rst",
    license="MIT",
    keywords="biology overhang dna",
    packages=find_packages(exclude="docs"),
    include_package_data=True,
    install_requires=[
        "matplotlib",
        "minotaor",
        "networkx",
        "numpy",
        "pdf_reports",
        "tatapov",
    ],
)
