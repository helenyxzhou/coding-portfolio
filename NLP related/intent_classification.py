import argparse
import os

import pandas as pd
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


def predict_intents(
    dataframe: pd.DataFrame(),
    text_column: str,
    tokenizer: AutoTokenizer,
    model: AutoModelForSequenceClassification,
    class_to_intent_mapping: dict = None,
) -> pd.DataFrame():
    """perform intent classification on a column of text of a given dataframe

    Args:
        dataframe: a dataframe,
        text_column: the name of the column that contains text data,
        tokenizer: tokenizer provided by a pre-trained model,
        model: a given pre-trained model,
        class_to_intent_mapping: a dictionary of intent indices and intents,
        if not available = None

    Returns:
        the original dataframe with a column of predicted intent
    """

    # Create an empty list to store the predicted intents
    predicted_intents = []

    # Iterate over the rows of the DataFrame without unpacking the index
    for _, row in dataframe.iterrows():
        user_input = row[text_column]

        # Tokenize and encode the user input
        encoded_input = tokenizer(
            user_input, return_tensors="pt", padding=True, truncation=True
        )

        # Perform inference
        logits = model(**encoded_input).logits
        predicted_class = logits.argmax().item()

        # Use the class-to-intent mapping obtained
        # from the model's configuration
        if class_to_intent_mapping:
            predicted_intent = class_to_intent_mapping.get(
                predicted_class, "Unknown"
            )
        else:
            predicted_intent = "Mapping not available"

        # Append the predicted intent to the list
        predicted_intents.append(predicted_intent)

    # Add the predicted intents as a new column in the DataFrame
    dataframe["predicted_" + text_column + "_intent"] = predicted_intents

    return dataframe


if __name__ == "__main__":
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(
            description="perform intent classification."
        )
        parser.add_argument("file", help="Path to the input CSV file")
        args = parser.parse_args()

        # Read the data from the CSV file into a DataFrame
        file_path = args.file

        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        # import the intent classification model from hugging face
        model_name = "qanastek/XLMRoberta-Alexa-Intents-Classification"
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Load the model's configuration
        config = AutoConfig.from_pretrained(model_name)

        # Read the file into a dataframe
        text_df = pd.read_csv(file_path)

        # Check if the model's config has labels
        if hasattr(config, "id2label"):
            class_to_intent_mapping = config.id2label
        else:
            class_to_intent_mapping = None

        if file_name == "clean_ACS_convo.csv":
            # Apply the predict_intents function to both columns
            text_df = predict_intents(
                text_df, "Text", tokenizer, model, class_to_intent_mapping
            )

        elif file_name == "clean_eduma_convo.csv":
            text_df = predict_intents(
                text_df, "user_input", tokenizer, model, class_to_intent_mapping
            )
            text_df = predict_intents(
                text_df,
                "chatbot_output",
                tokenizer,
                model,
                class_to_intent_mapping,
            )

        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Specify the relative path to the "data" directory
        data_directory = os.path.join(script_directory, "..", "data")

        # Specify the path to the output text file within the "data" directory
        output_file_path = os.path.join(data_directory, "intent_" + file_name)

        text_df.to_csv(output_file_path, index=False)

        print(
            "Intent classification for "
            + file_name
            + " has been saved to"
            + output_file_path
        )

    except Exception as e:
        # Print the error message if an exception occurs
        print(f"An error occurred: {str(e)}")
