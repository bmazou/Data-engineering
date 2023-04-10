## Requirements
- Python 3, ideally 3.10
- `rdflib` module

## Instalation
- With Python installed, run `pip install -r requirements.txt`

## Description
- To generate provenance for the population datacube, run `python population_prov.py --file_name file_name.trig`
- To generate care providers provenance, run `python care_providers_prov.py --file_name file_name.trig`
- The trig files will be saved into `output/` directory
- The two scripts share several common functions. They are inside `prov_utils.py`