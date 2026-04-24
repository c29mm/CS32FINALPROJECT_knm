from collections import Counter # dictionary that automatically counts

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
    counts = parse_script("sample_TDK_script.txt")
    print_summary(counts)
