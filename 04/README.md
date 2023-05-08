## Requirements
- Python 3, ideally 3.10
- `rdflib` module

## Instalation
- With Python installed, run `pip install -r requirements.txt`
## Description
- **SKOS hierarchy** is generated through `create_skos_hierarchy` function inside `my_utils/utils.py`.
  - `population.py` and `care_providers.py` now call this function to create said hierarchy.
- **Dcat dataset** for the *population* datacube is created by running `python population_dcat.py`
  - The result is saved into `output/population_dcat.ttl`