from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iatiutils",
    version="1.0.0",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/OpenDataServices/iati-utils",
    description="An IATI data utility library",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
      "lxml",
      "requests",
      "click"
    ],
    entry_points={
        'console_scripts': [
            'merge_indicator = iatiutils.merge_indicator:merge_indicator',
            'sort_iati = iatiutils.sort_iati:sort_iati',
            'country_lookup = iatiutils.country_lookup:country_lookup'
        ],
},
)
