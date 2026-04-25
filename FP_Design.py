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
        print("API Error:", data.get("Error"))
        return None

    ratings = data.get("Ratings", [])

    # try to find Rotten Tomatoes rating
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return f"Rotten Tomatoes: {rating['Value']}"

    # fallback to IMDb rating if Rotten Tomatoes is unavailable
    if data.get("imdbRating") and data["imdbRating"] != "N/A":
        return f"IMDb: {data['imdbRating']}/10"

    # if nothing is available
    return "No rating available"

def clean_character_name(name):
    # remove extra whitespace
    name = name.strip()

    # ignore obvious title or scene divider lines
    if "SCENE" in name or "_" in name:
        return None

    # remove quotation marks around titles/names
    name = name.replace('"', "")

    # combine alternate names for the same major characters
    aliases = {
        "BOB (MR. INCREDIBLE)": "BOB",
        "MR. INCREDIBLE": "BOB",
        "HELEN (ELASTIGIRL)": "HELEN",
        "ELASTIGIRL": "HELEN",
        "LUCIUS (FROZONE)": "LUCIUS",
        "FROZONE": "LUCIUS",
        "BUDDY (INCREDIBOY)": "BUDDY",
    }

    return aliases.get(name, name)

def parse_script(filepath):
    # read file and strip empty lines
    with open(filepath, "r") as f: # open in read mode
        lines = [line.strip() for line in f if line.strip()] # remove whitespace + skip empty lines

    counts = Counter()        # stores dialogue count per character
    current = None            # current speaker
    has_dialogue = False      # whether we've seen dialogue after speaker

    for line in lines:
        if line.isupper():    # this line is a speaker name
            if current is not None and has_dialogue:
                counts[current] += 1   # count previous speaker block

            current = clean_character_name(line)             # update speaker
            has_dialogue = False       # reset dialogue flag

        else:
            has_dialogue = True        # this line is dialogue

    # catch the last speaker block
    if current is not None and has_dialogue:
        counts[current] += 1

    return counts


def print_summary(counts):
    # handle case where no characters were detected
    if not counts:
        print("No characters detected.")
        return

    # calculate total dialogue blocks across all characters
    total_dialogue = sum(counts.values())

    # find the character with the most dialogue
    most_talkative = counts.most_common(1)[0]

    # print all detected characters
    print("Characters detected:", ", ".join(counts.keys()))

    # print the most talkative character
    print(f"\nMost talkative character: {most_talkative[0]} ({most_talkative[1]} dialogue blocks)")

    # print dialogue count and percentage for each character
    print("\nDialogue by Character:")
    for character, count in counts.most_common():
        percent = (count / total_dialogue) * 100  # compute percentage of total dialogue
        print(f"{character}: {count} dialogue blocks ({percent:.1f}%)")

if __name__ == "__main__":
    api_key = "b621eeaf"
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

