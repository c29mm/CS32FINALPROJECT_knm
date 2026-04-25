from collections import Counter # dictionary that automatically counts
import requests #helpful for connecting to rankings site

def get_online_rating(movie_title, api_key):
    url = "http://www.omdbapi.com/"
    params = {
        "t": movie_title,
        "apikey": api_key
    }

    response = requests.get(url, params = params)
    data = response.json()

    if data.get("Response") == "False":
        return None

    ratings = data.get("Ratings", [])

    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]
    return None

def parse_script(filepath):
    # read file and strip empty lines
    with open(filepath, "r") as f: # open in read mode
        lines = [line.strip() for line in f if line.strip()] # remove whitespace + skip empty lines

    counts = Counter()        # stores dialogue count per character
    current = None            # current speaker
    has_dialogue = False      # whether we've seen dialogue after speaker

    for line in lines:
        if line.isupper():    # this line is a speaker name
            if current and has_dialogue:
                counts[current] += 1   # count previous speaker block

            current = line             # update speaker
            has_dialogue = False       # reset dialogue flag

        else:
            has_dialogue = True        # this line is dialogue

    # catch the last speaker block
    if current and has_dialogue:
        counts[current] += 1

    return counts


def print_summary(counts):
    # print all detected characters
    print("Characters detected:", ", ".join(counts.keys()))

    # print dialogue count for each character
    for character in counts:
        print(f"{character}: {counts[character]} dialogue blocks")

if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"
    movie = input("Enter movie title: ")

    rating = get_online_rating(movie, api_key)

    if rating:
        print(f"Rotten Tomatoes rating for {movie}: {rating}")
    else:
        print("Rotten Tomatoes rating not found.")
    script_file = input("Enter script file name: ")
    try:
        counts = parse_script(script_file)
        print_summary(counts)
        num_characters = len(counts)
        total_dialogue = sum(counts.values())

        print("\nComplexity Metrics:")
        print(f"Number of characters: {num_characters}")
        print(f"Total dialogue blocks: {total_dialogue}")
        
    except FileNotFoundError:
        print("Error: Script file not found.")

