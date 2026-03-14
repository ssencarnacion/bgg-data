import xml.etree.ElementTree as ET
import os
import re
import json  

# PARSER VERSION 7: 
# Returns a JSON-like dict with username and game ratings
# Disregards malformed XML files
# Escapes ampersand characters
# Disregards XML files with <errors> root
# Handles multiple versions of the same game using objectid
# Handles XML files with missing or non-numeric ratings

def escape_ampersands(xml):
    # Replace & with &amp; only if not part of an existing entity
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml)

def parser(filepath):
    # extract username from filename
    username = os.path.basename(filepath).split("username=")[1].split("&")[0].split(".xml")[0]

    # read file and escape ampersands
    xml_content = open(filepath, encoding="utf-8").read()
    xml_content = escape_ampersands(xml_content)

    # catch-all: do nothing if XML is malformed
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return None
        
    # parse XML and extract games and their respective ratings
    items = root.findall("item")

    # stop parsing if root element is <errors>
    if root.tag != "items":
        return None

    # override filename username if XML root provides one
    xml_username = root.get("username")
    if xml_username:
        username = xml_username

    # store highest rating per game ID
    ratings_by_id = {}

    for item in items:
        game_id = item.get("objectid")
    
        # skip items without objectid
        if not game_id:
            continue

        # attempt to parse rating, use None if missing/invalid
        rating_value = None
        rating_elem = item.find("stats/rating")

        if rating_elem is not None:
            try:
                rating_value = float(rating_elem.get("value"))
            except (TypeError, ValueError):
                pass  # leave as None if value is nonnumeric

        # store highest rating per game ID
        existing_rating = ratings_by_id.get(game_id)

        if existing_rating is None:
            ratings_by_id[game_id] = rating_value

        # update only if new rating is numeric and higher
        elif rating_value is not None and rating_value > existing_rating:
            ratings_by_id[game_id] = rating_value

    # create the JSON-like dict
    result = {
        "username": username,
        "games": ratings_by_id
    }

    return result

