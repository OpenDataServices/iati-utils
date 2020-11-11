from setuptools import setup

setup(
    name = "iatiutils",
    version = "0.0.1",
    author = "Open Data Services Co-operative",
    author_email = "code@opendataservices.coop",
    description = ("Tools for working with IATI data."),
    license = "MIT",
    url = "https://github.com/OpenDataServices/iati-utils",
    packages=["iatiutils"],
    install_requires=["Click", "lxml", "requests"],
    extras_require={
        "test": ["pytest"]
    },
    entry_points="""
        [console_scripts]
        iatiutils=iatiutils.cli:cli
    """,
)