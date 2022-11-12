from typing import List


def display_frquency_table(words: List[str], take=100):
    table = {}
    for word in words:
        if word not in table:
            table[word] = 0
        table[word] += 1
    
    l = list(sorted(table.items(), key=lambda kv: kv[1], reverse=True))
    for i in range(0, min(take, len(l))):
        w, c = l[i]
        print(c, w)


def print_words(words: List[str]):
    for w in words:
        print(w, end=" ")
    print()
