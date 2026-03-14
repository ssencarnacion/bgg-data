# bgg-data

A simple web application that computes a similarity score between two
BoardGameGeek users based on their board game ratings.

The project parses BoardGameGeek XML rating exports, converts them into
structured JSON files, and compares users based on overlapping game ratings.

## Features

### `parser_v7.py`

- Relies on the **ElementTree** module to parse information from XML files
- Extracts a username and the list of games, along with their respective ratings, from the user's collection
- Stores this parsed data into a dictionary

### `json_loader.py`

- Iterates through all XML files in the `data/` directory that matches a certain filename pattern
- Only the files with filenames starting with `collection@stats=1&subtype=boardgame&username=<username>` will be processed
- Uses `parser_v7.parser()` to convert each valid XML file into a structured Python dictionary
- Skips files that are malformed or contain an unexpected root element (e.g., <errors>)
- Writes the parsed results as formatted JSON files to the `parsed_data/` directory, one per user

### `app.py`

- Uses Flask to provide a simple web interface for selecting two BoardGameGeek users from parsed JSON data
- Loads user rating data from the `parsed_data/` directory and computes taste similarity using Pearson correlation
- Normalizes the similarity score to a 0–1 range and applies a confidence adjustment based on the number of overlapping games
- Displays the similarity score and the count of commonly rated games directly in the browser

## Requirements

- Python 3.9 or higher
- Flask

Install dependencies using pip:

```
pip install flask
```

## Running the Program

Ensure that all raw BoardGameGeek XML files are placed inside the `/data` folder. <br>
Run the parser to convert XML files into JSON. Parsed JSON files will be saved inside the `/parsed_data` folder. <br>
The terminal will show you more information regarding which files were successfully processed.

```
python json_loader.py
```


## Running the Web App

Once the data has been parsed, start the Flask application:

```
python app.py
```

<img width="1095" height="181" alt="image" src="https://github.com/user-attachments/assets/c7dec0b7-4e8a-4a73-9811-3a125ee27e75" />

Once the data has been parsed, start the Flask application. Open your browser and navigate to:

```
localhost:5000
```

<img width="1638" height="312" alt="image" src="https://github.com/user-attachments/assets/52b3fdba-2a60-472e-b5f3-92642a21f4cf" />
