"""Used to filter out ill or bad formatted text.

Instructions:
```bash
cat books.jsonl | python filter_out_bad_lines.py > clean_books.jsonl
```
"""

import argparse
import sys
import json

from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser("Filter out bad lines.")
    parser.add_argument("--output_bad_lines", default="bad_lines.jsonl", help="output file for bad lines")

    args = parser.parse_args()

    return args


def is_bad_line(line):
    ending_punctuations = ["。", "！", "？", "……", "”", "："]
    if not any(line.endswith(punc) for punc in ending_punctuations):
        return True

    if len(line) < 5 or len(line) > 500:
        return True

    # TODO: add ill character filtering
    # ill_word_regex = "[-]|□|■|\*"
    # if re.search(ill_word_regex, line) != None:
    #     return True

    return False


def is_bad_doc(doc):
    count = 0
    for bad_word in open("bad_words.list"):
        bad_word = bad_word.strip()
        if bad_word in doc:
            count += doc.count(bad_word)
            if count > 3:
                return True

    return False


def main():
    args = parse_args()
    bad_lines_file = open(args.output_bad_lines, "wt")
    bad_words = []
    for word in open("bad_words.list"):
        bad_words.append(word)

    for line in tqdm(sys.stdin):
        try:
            j = json.loads(line)
        except:
            continue

        if is_bad_doc(j["text"]):
            print(json.dumps(j, ensure_ascii=False), file=bad_lines_file)
            continue

        output = []
        bad_lines = []
        for line in j["text"].splitlines():
            line = line.strip()
            if is_bad_line(line):
                bad_lines.append(line)
            else:
                output.append(line)

        if len(output) > 5:
            j["text"] = '\n'.join(output)
            print(json.dumps(j, ensure_ascii=False))
        else:
            bad_lines += output

        if len(bad_lines) > 0:
            j["text"] = '\n'.join(bad_lines)
            print(json.dumps(j, ensure_ascii=False), file=bad_lines_file)


if __name__ == "__main__":
    main()
