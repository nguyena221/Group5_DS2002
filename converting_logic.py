#!/usr/bin/env python3
import json
import csv
import io

def get_value(container, key):
    """
    Helper function used in convert_json function.
    Used for in case the nested key of nutrients is NaN so there will be no error given trying to get values from NaN.
    """
    try:
        return container.get(key, "")
    except Exception:
        return ""

def flatten_json(json_data):
    """
    Called by convert_json_to_csv function.
    Takes in the json file and flattens it.
    In case any data cannot be retrieved, just puts a blank in its place.
    """
    json_flattened = []

    for recipe_id, recipe_data in json_data.items():
        nutrients = recipe_data.get("nutrients", {})

        try:
            ingredients = " | ".join(recipe_data.get("ingredients", []))
        except Exception:
            ingredients = ""

        try:
            instructions = " ".join(recipe_data.get("instructions", []))
        except Exception:
            instructions = ""

        recipe = {
            "ID": recipe_id,
            "Continent": recipe_data.get("Contient", ""),
            "Country_State": recipe_data.get("Country_State", ""),
            "Cuisine": recipe_data.get("cuisine", ""),
            "Title": recipe_data.get("title", ""),
            "Url": recipe_data.get("URL", ""),
            "Rating": recipe_data.get("rating", ""),
            "Total_Time": recipe_data.get("total_time", ""),
            "Prep_Time": recipe_data.get("prep_time", ""),
            "Cook_Time": recipe_data.get("cook_time", ""),
            "Description": recipe_data.get("description", ""),

            "Ingredients": ingredients,
            "Instructions": instructions,

            "Calories": get_value(nutrients, "calories"),
            "Carbs": get_value(nutrients, "carbohydrateContent"),
            "Cholesterol": get_value(nutrients, "cholesterolContent"),
            "Fiber": get_value(nutrients, "fiberContent"),
            "Protein": get_value(nutrients, "proteinContent"),
            "Saturated_Fat": get_value(nutrients, "saturatedFatContent"),
            "Sodium": get_value(nutrients, "sodiumContent"),
            "Sugar": get_value(nutrients, "sugarContent"),
            "Fat": get_value(nutrients, "fatContent"),
            "Unsaturated_Fat": get_value(nutrients, "unsaturatedFatContent"),

            "Serves": recipe_data.get("serves", ""),
        }

        json_flattened.append(recipe)

    return json_flattened


def convert_json_to_csv(json_data):
    """
    Calls flatten_json function to get flattened json.
    Turns that into csv in form of string to be used by Lambda to store into csv file in S3 bucket
    """
    json_flattened = flatten_json(json_data)

    output = io.StringIO()

    writer = csv.DictWriter(output, fieldnames=json_flattened[0].keys())
    writer.writeheader()
    writer.writerows(json_flattened)

    return output.getvalue()
