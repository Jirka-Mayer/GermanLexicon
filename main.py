from typing import List, Dict, Tuple
import os
from app.closed_classes import *
from app.NounAdjectiveProcessor import NounAdjectiveProcessor
import app.ui
import app.io
from app.extract_weak_verbs import extract_weak_verbs
from app.extract_noun_plural_classes import extract_noun_plural_classes


################
#     MAIN     #
################

def main():
    corpus_file_path = "data/de-tagged.txt.gz"

    if not os.path.isfile(corpus_file_path):
        print("The file {} does not exist.".format(corpus_file_path))
        print()
        print("Download the file by executing:")
        print(
            "    wget -O data/de-tagged.txt.gz https://ufal.mff.cuni.cz" +
            "/~zeman/vyuka/morfosynt/lab-lexicon/de-tagged.txt.gz"
        )
        return


    print()
    print("==========================================")
    print("Extracting open classes from untagged data")
    print("==========================================")
    print()

    # print("Loading words...")
    # words = app.io.load_words("data/de-tagged.txt.gz", limit=None)

    # print("Extracting verbs...")
    # weak_verbs = extract_weak_verbs(words)
    # app.io.write_verbs("data/lexicon-weak-verbs.txt.gz", weak_verbs)

    # print("Extracting nouns and adjectives...")
    # p = NounAdjectiveProcessor(words)
    # p.run()
    # app.io.write_words("data/lexicon-nouns.txt.gz", set(p.nouns))
    # app.io.write_words("data/lexicon-adjectives.txt.gz", set(p.adjectives))


    print()
    print("===============================================================")
    print("Extracting lexicons for morphological analyzer from tagged data")
    print("===============================================================")
    print()

    print("Loading tagged words...")
    tagged_words = app.io.load_tagged_words("data/de-tagged.txt.gz")

    print("Extracting noun plural classes...")
    noun_classes = extract_noun_plural_classes(tagged_words)

    print("Counts:")
    for k, v in noun_classes.items():
        print(" ", k.ljust(15), len(v))

    filename = "data/tagged-lexicon-nouns.lexc"
    print("Saving to '{}'...".format(filename))
    with open(filename, "w") as f:
        f.write("LEXICON Noun\n")
        for k, v in noun_classes.items():
            for word in sorted(v):
                f.write("{} {};\n".format(word, k))

    print("Done.")


main()
