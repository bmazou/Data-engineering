import csv

def load_from_csv(path):
    with open(path, "r", encoding="utf8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  
        for line in reader:
            yield {key: value for key, value in zip(header, line)}
          
def filter_dem0004_county(data):
    for row in data:
        contains_mean_value = row["vuk"] == "DEM0004"
        is_county = row["vuzemi_cis"] == "101"
        if contains_mean_value and is_county:
            yield row      
    
def load_nuts_codes(path):
    codes = {}
    with open(path, "r", encoding="utf8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  
        for line in reader:
            end_of_file = len(line) == 0
            if end_of_file:
                break
            
            code_pos = -2
            vuzemi_kod = line[code_pos]

            nuts_pos = 4
            nuts = line[nuts_pos]
            
            codes[vuzemi_kod] = nuts
    
    return codes

def convert_vuzemi2nuts(nuts_codes, vuzemi_code):
    if vuzemi_code in nuts_codes:
        okres_code = nuts_codes[vuzemi_code]
        kraj_code = okres_code[:-1]

        return okres_code, kraj_code
    
    else:
        raise ValueError(f"Vuzemi code \'{vuzemi_code}\' not found in the nuts codes")
    
def filter_data(data):
    data = filter_dem0004_county(data)
    nuts_codes = load_nuts_codes("data/ciselnik-okresu.csv")

    ret = {}
    for row in data:
        vuzemi_kod = row["vuzemi_kod"]
        okres_code, kraj_code = convert_vuzemi2nuts(nuts_codes, vuzemi_kod)
        
        dimension = f'{okres_code}---{kraj_code}'
        value = row["hodnota"]
        ret[dimension] = value
        
    return ret
    
            
def load_data(path):
    data = load_from_csv(path)
    
    return filter_data(data)
