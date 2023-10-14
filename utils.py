import logging
from dotenv import load_dotenv
import tiktoken
import math

def is_valid_query(query):
    """
    Validates whether a string is a valid query by applying a series of checks using if statements.

    Args:
        query (str): The string to validate.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    if query is None:
        return False

    if not query.strip():
        return False

    # Additional checks can be added here using more if statements

    return True

def is_all_none(arr):
    return all(element is None for element in arr)

def load_environment(file_path=".env"):
    """
    Load environment variables using python-dotenv.

    :param file_path: Path to the .env file
    :type file_path: str
    """
    # Load the .env file
    if load_dotenv(dotenv_path=file_path):
        logging.info("Successfully loaded environment variables from .env file.")
    else:
        logging.error(f"Failed to load .env file from {file_path}")

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def divide_and_round_up(dividend, divisor):
    result = math.ceil(dividend / divisor)
    return result

def chunk_array(arr, num_of_chunks):
    """
    Splits an array into a specified number of roughly equal-sized chunks.

    Parameters:
    arr (list): The list to be divided.
    num_of_chunks (int): The number of chunks to divide the list into.

    Returns:
    list: A list of chunks (sub-lists).
    """

    # Initialize an empty list to hold the chunks
    chunks = []

    # Check for invalid inputs and log accordingly
    if not arr or num_of_chunks <= 0:
        logging.error("Invalid input. Please provide a non-empty array and a positive integer for num_of_chunks.")
        return chunks

    avg_chunk_size = len(arr) // num_of_chunks  # Calculate average chunk size
    remainder = len(arr) % num_of_chunks  # Calculate the remainder

    start = 0  # Initialize start index for slicing

    # Loop to create each chunk
    for i in range(num_of_chunks):
        end = start + avg_chunk_size  # Calculate end index for slicing

        # Distribute the remainder among the first 'remainder' chunks
        if remainder > 0:
            end += 1
            remainder -= 1

        # Create a chunk and append it to the list of chunks
        chunk = arr[start:end]
        chunks.append(chunk)

        logging.info(f"Created chunk {i+1}: {chunk}")

        # Update the start index for the next iteration
        start = end

    return chunks