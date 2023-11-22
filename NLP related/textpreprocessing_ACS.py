import argparse
import os

import pandas as pd
import textpreprocessing_functions

if __name__ == "__main__":
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="clean conversation data.")
        parser.add_argument("file", help="Path to the input CSV file")
        args = parser.parse_args()

        # Read the data from the CSV file into a DataFrame
        file_path = args.file

        if file_path == "../data/structured_ACS_by_convo.json":
            convo_df = pd.read_json(
                file_path, dtype={"Timestamps": "datetime64[ms]"}
            )
            # Extract the text column
            clean_df = convo_df.copy()

            # Clean the texts in the column
            clean_df["Messages"] = clean_df["Messages"].apply(
                lambda x: [
                    textpreprocessing_functions.clean_text(item) for item in x
                ]
            )

            # discard any empty/NA items
            clean_df["Messages"] = clean_df["Messages"].apply(
                lambda text_list: [
                    item for item in text_list if item != "NA" and item != ""
                ]
            )

        else:
            text_df = pd.read_json(file_path)
            # Extract the text column
            clean_df = text_df.copy()

            # Clean the texts in the column
            clean_df["Text"] = clean_df["Text"].apply(
                lambda x: [
                    textpreprocessing_functions.clean_text(item) for item in x
                ]
            )

            # discard any empty/NA items
            clean_df["Text"] = clean_df["Text"].apply(
                lambda text_list: [
                    item for item in text_list if item != "NA" and item != ""
                ]
            )

        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Specify the relative path to the "data" directory
        data_directory = os.path.join(script_directory, "..", "data")

        # Specify the path to the output text file within the "data" directory
        output_file_path = os.path.join(
            data_directory, "clean_ACS_convo_full.json"
        )

        clean_df.to_json(output_file_path, index=False)

        print(
            "Cleaned conversation content has been saved to" + output_file_path
        )

    except Exception as e:
        # Print the error message if an exception occurs
        print(f"An error occurred: {str(e)}")
