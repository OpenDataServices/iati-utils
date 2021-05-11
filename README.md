# IATI Utilities

## Description

This package represents a collection of utilities for reorganising IATI data.

## Instructions

Install the core requirements:
```bash
# Create a virtual environment
python3 -m venv .ve
source .ve/bin/activate
pip install -r requirements.txt
```

You can also install the package locally with:
```bash
python setup.py install
```

The commands can be run from the command line with the following commands after local install:

```bash
sort_iati --help
merge_indicators --help
country_lookup --help
```

The commands can also be imported with the following commands:

```python
from iatiutils import sort_iati 
# or
from iatiutils import merge_indicators
#or
from iatiutils import country_lookup
```
