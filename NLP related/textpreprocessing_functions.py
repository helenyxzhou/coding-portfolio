import ast
import re

import pandas as pd


def clean_text(text: str) -> str:
    """Performs general text processing by
       removing punctuation, newline characters,
       lowercasing, and stripping sentences.

    Args:
        text: a sentence or a paragraph

    Returns:
        The cleaned text with punctuation, newline characters removed,
        lowercased, and stripped.
    """
    try:
        # Remove newline characters
        text = text.replace("\n", "")

        # Remove punctuation (including upside-down ! and ?)
        cleaned_text = re.sub(r"[!¡?¿.,;*]", "", text)

        # Lowercase the text and strip it
        cleaned_text = cleaned_text.lower().strip()

        return cleaned_text
    except Exception:
        return "NA"


def clean_text_eng(text: str) -> str:
    """performs general text processing
       split sentences into individual words,
       remove punctuation,
       lower case,
       and filter out non-English words

    Args:
        text: a sentence or a paragraph

    Returns:
        a list of standardized words or "NA" if no words satisfy the criteria
    """

    try:
        # Split the paragraph into sentences
        sentences = re.split(r"(?<=[.!?])\s*", text)

        cleaned_words = []
        for sentence in sentences:
            # Split each sentence into words
            words = re.split(r"\s+", sentence)

            # Filter for English words and emojis
            english_words_and_emojis = [
                word
                for word in words
                if re.search(
                    r"[a-zA-Z🙂🙃]", word
                )  # Adjust the regex to include emojis
            ]

            # Remove punctuation, lowercase, and strip each word
            cleaned_words.extend(
                [
                    re.sub(r"[!.,;?]", "", word).lower().strip()
                    for word in english_words_and_emojis
                ]
            )

        if not cleaned_words:  # Check if the list is empty
            return "NA"
        else:
            return cleaned_words
    except Exception:
        return "NA"


def combine_lists(sublists: list) -> list:
    """flattens a list of lists into one list
    Args:
        sublists: a list of lists

    Returns:
        a single list
    """
    return [item for sublist in sublists for item in sublist]


def try_literal_eval(input_str: str) -> list:
    """parse a string formatted list as a list

    Args:
        input_str: a string formatted as a list

    Returns:
        a list

    Raise:
        error if the string is malformed
    """

    try:
        return ast.literal_eval(input_str)

    except (ValueError, SyntaxError) as e:
        print(f"Malformed string: {input_str}")
        raise e


def clean_df(df: pd.DataFrame(), col_name: str) -> pd.DataFrame():
    """perform textpreprocessing on a dataframe of conversation content

    Args:
        df: a dataframe of conversation content
        col_name: the name of the column

    Returns:
        a cleaned dataframe with no "NA" values and standardized words
    """

    # Apply the clean_text function to the DataFrame
    df_copy = df.copy()
    df_copy[col_name] = df_copy[col_name].apply(clean_text_eng)

    # drop all rows with NA values
    clean_df = df_copy[df_copy.ne("NA").all(axis=1)]

    return clean_df
