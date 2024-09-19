# Assignment


# Repository Structure
Function_Summarization.py: This script analyzes each Python function in the target repository and generates summaries, code snippets, and Abstract Syntax Trees (ASTs) for the functions. It orders the function summaries based on dependencies, ensuring that if Function A depends on Function B, Function B is summarized first.

Search_Mechanism.py: This script implements a search mechanism to navigate through the codebase. It allows you to locate specific data types (e.g., int, str, float, etc.) or search for specific function implementations and references within the code.

How to Use
1. Function Summarization
To run the function summarization on a repository:

Clone the repository you want to analyze.
Run the Function_Summarization.py script:
bash
Copy code
python Function_Summarization.py
The script will generate summaries of the functions and output them in a structured JSON file for reference.
2. Search Mechanism
To run the search mechanism:

Navigate to the repository you want to search.
Run the Search_Mechanism.py script:
bash
Copy code
python Search_Mechanism.py
You can modify the search parameters within the script to search for specific data types or functions. The results will list where the elements are used within the codebase.
