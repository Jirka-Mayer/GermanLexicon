import gzip


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
