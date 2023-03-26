import csv

def load_from_csv(path):
    with open(path, "r", encoding="utf8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  
        for line in reader:
            yield {key: value for key, value in zip(header, line)}
          
def filter_data(data, desired_cols):
    for row in data:
        yield {col: row[col] for col in desired_cols}
      
def count_obor_pece(data):
    result = {}
    for row in data:
        if row["OborPece"] == "": 
            continue
        
        obory = [obor.strip().lower() for obor in row["OborPece"].split(",")]
        # Filter out duplicates
        obory = list(set(obory))
        
        for obor in obory:
            dimension = f'{row["OkresCode"]}---{row["KrajCode"]}---{obor}'
            if dimension in result:
                result[dimension] += 1
            else:
                result[dimension] = 1
            
    return result
      
            
def load_data(path):
    data = load_from_csv(path)
    
    desired_cols = ["KrajCode", "OkresCode", "OborPece"]
    filtered_data = filter_data(data, desired_cols)

    counts = count_obor_pece(filtered_data)
    return counts


