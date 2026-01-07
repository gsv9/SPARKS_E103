import json

def load_data(filename):
    with open(f"data/{filename}", "r") as f:
        return json.load(f)
