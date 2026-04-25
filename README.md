# CS32FINALPROJECT_knm

Our project analyzes movie scripts in .txt format by parsing dialogue to extract and quantify character-based metrics. Specifically, we aim to identify the number of distinct characters, measure interaction frequency between characters, calculate the proportion of dialogue attributed to each character, and track how often characters reference one another in conversation. These metrics serve as a proxy for narrative and character complexity. We will then compare these quantitative measures against external ratings from sources such as IMDb and Rotten Tomatoes to investigate whether there is any correlation between script-level complexity and audience or critical reception.

## Features
- Detects all characters in a script
- Counts how many dialogue blocks each character has
- Computes the percentage of dialogue attributed to each character
- Identifies the most talkative character
- Calculates overall complexity metrics:
  - Number of characters
  - Total dialogue blocks
- Fetches movie ratings using the OMDb API (Rotten Tomatoes preferred, IMDb fallback)

---

## Requirements
- Python 3
- `requests` library

Install required package with:
```bash
pip install requests
