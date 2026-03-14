import os
import json
from parser_v7 import parser

# made with ChatGPT https://chatgpt.com/s/t_6969f895a4848191b14cd840d5526042
# source and output folders
DATA_DIR = "data"
OUTPUT_DIR = "parsed_data"

# make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# define the filename pattern to match relevant files
# they all start with 'collection@stats=1&subtype=boardgame&username='
FILENAME_PREFIX = "collection@stats=1&subtype=boardgame&username="

# loop through files in data folder
for filename in os.listdir(DATA_DIR):
    if filename.startswith(FILENAME_PREFIX) and filename.endswith(".xml"):
        filepath = os.path.join(DATA_DIR, filename)

        # run parser
        result = parser(filepath)

        if result is not None:
            # save JSON output
            username = result["username"]
            output_path = os.path.join(OUTPUT_DIR, f"{username}.json")
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Parsed and saved: {username}.json")
        else:
            print(f"Skipped (malformed or incorrect root): {filename}")
