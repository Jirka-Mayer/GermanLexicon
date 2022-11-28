import gzip
from typing import Dict, Set


def load_words(filename, limit=None):
    words = []
    with gzip.open(filename, "rb") as f:
        i = 0
        while True:
            if limit is not None and i > limit:
                break
            i += 1
            
            line = f.readline()
            if line == b"":
                break

            if line == b"\n":
                continue
            
            line = str(line, "UTF-8")
            word_length = line.index("\t")
            word = line[:word_length]
            words.append(word)
    return words


def load_tagged_words(filename, limit=None) -> Set[str]:
    tagged_words = set()
    with gzip.open(filename, "rb") as f:
        i = 0
        while True:
            if limit is not None and i > limit:
                break
            i += 1
            
            line = f.readline()
            if line == b"":
                break

            if line == b"\n":
                continue
            
            line = str(line, "UTF-8")
            word_length = line.index("\n")
            word = line[:word_length]
            tagged_words.add(word)
    return tagged_words


def write_verbs(filename: str, verbs: Dict[str, set]):
    with gzip.open(filename, "wb") as f:
        for verb, cluster in sorted(verbs.items(), key=lambda x: x[0]):
            lexemes = " ".join(sorted(cluster))
            line = "{}\t{}\n".format(verb, lexemes)
            f.write(bytes(line, "UTF-8"))

def write_words(filename: str, words: Set[str]):
    with gzip.open(filename, "wb") as f:
        for word in sorted(words):
            line = "{}\n".format(word)
            f.write(bytes(line, "UTF-8"))
