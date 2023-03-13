<!-- Add system requirements as python 3.10 and rdflib, csv packages -->
## Requirements
- Python 3, ideally 3.10
- rdflib module

## Instalation
- With Python installed, run `pip install rdflib`

## Description
- Used data are stored in `data` folder
- Generated ttl files are stored in `output` folder
- To run first script, run `python care_providers.py`
- Second script is run with `python population.py`
- Both scripts use their own csv data loader, and share several utilities for creating the data cubes.
- Tests are run automatically and are handled by `validator.py`, that runs the desired SPARQL queries  