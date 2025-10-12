#!/usr/bin/env python3

import sys
import requests

# Architectural choice: Hardcoding the server URL is suitable for this specific
# client-server pair. For more flexibility, this could be read from an
# environment variable or a command-line argument.
SERVER_URL = "http://127.0.0.1:8000/translate"

def main():
    """
    Reads text from stdin, sends it to the translation server,
    and prints the result to stdout.
    """
    # Reading from sys.stdin allows the script to be used in pipelines,
    # for example: cat japanese_text.txt | python cli.py
    japanese_text = sys.stdin.read().strip()

    if not japanese_text:
        print("Error: No input provided. Please pipe text to the script.", file=sys.stderr)
        sys.exit(1)

    payload = {"text": japanese_text}

    try:
        # The 'requests' library is used for its simplicity and robustness
        # in handling HTTP client-side operations.
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()  # This will raise an exception for 4xx/5xx responses

        response_data = response.json()
        print(response_data["translation"])

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the translation server at {SERVER_URL}.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print("Error: Received an unexpected response from the server.", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
