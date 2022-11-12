from typing import List, Dict
from app.closed_classes import is_closed_class
from app.fset import fset


def longest_common_subword(words: set) -> str:
    best = ""
    best_len = 0
    
    subject = min(words, key=len)
    for i in range(len(subject)):
        for j in range(i + 1, len(subject) + 1):
            if j - i <= best_len:
                continue
            candidate = subject[i:j]
            if all((candidate in w) for w in words):
                best = candidate
                best_len = len(candidate)

    return best


def extract_weak_verbs(words: List[str]):
    # set of all open-class lexemes composed of only letters
    # that begin with a lowercase letter (are more likely to be verbs)
    lexemes = fset(
        w for w in words
        if w.isalpha()
        and w[0].islower()
        and not is_closed_class(w)
    )

    # Possible inflections of the verb "(ein)kaufen"
    #
    # Infinitive
    # kauf-en
    #
    # Present tense
    # ich kauf-e   wir kauf-en
    # du  kauf-st  ihr kauf-t
    # er  kauf-t   sie kauf-en
    #
    # Future tense
    # ich werde kauf-en
    #
    # Past tense
    # ich habe/bin ge-kauf-t
    # ich kauf-te
    #
    # Imperative
    # Kauf das!
    #
    # These are all the forms:
    # kauf
    # kauf-e
    # kauf-en
    # kauf-t
    # kauf-te
    # kauf-st
    # ge-kauf-t
    #
    # Remove separable prefixes
    # http://germanforenglishspeakers.com/verbs/prefix-verbs/
    # ein-kauf-en
    # ein-ge-kauf-t
    # ich kauf-e ein

    def separate_prefix(word: str):
        # https://learn-german-easily.com/german-prefix
        if word[:6] in ["zurück"]:
            return word[:6], word[6:]
        if word[:4] in ["nach"]:
            return word[:4], word[4:]
        if word[:3] in ["auf", "aus", "bei", "ein", "los", "mit", "hin", "her", "vor", "weg"]:
            return word[:3], word[3:]
        if word[:2] in ["an", "ab", "zu"]:
            return word[:2], word[2:]
        return "", word

    def get_possible_roots(word: str):
        prefix, root = separate_prefix(word)
        if root[-1:] in ["e", "t"]:
            yield root[:-1]
        if root[-2:] in ["en", "te", "st"]:
            yield root[:-2]
        if root[:2] == "ge" and root[-1:] == "t":
            yield root[2:-1]
        yield root
        if prefix != "":
            yield prefix + root

    def get_possible_forms(word: str):
        prefix, root = separate_prefix(word)
        yield prefix + root
        yield root + "e"
        yield root + "en"
        yield root + "t"
        yield root + "te"
        yield root + "st"
        yield prefix + "ge" + root + "t"

    def find_alternative_forms(word: str):
        found_forms = set()
        for root in get_possible_roots(word):
            for form in get_possible_forms(root):
                if len(form) <= 3: # short forms are probably not verbs
                    continue
                if form in lexemes:
                    found_forms.add(form)
        return found_forms

    def find_cluster_root(cluster: set):
        #return longest_common_subword(cluster) # does not work as well
        candidates = (
            root
            for word in cluster
            for root in get_possible_roots(word)
        )
        return min(candidates, key=len)

    def find_prefixed_roots(root: str, cluster: set):
        prefixes = [
            "zurück", "nach", "auf", "aus", "bei", "ein", "los",
            "mit", "hin", "her", "vor", "weg", "an", "ab", "zu"
        ]
        prefixed_roots = dict()
        for prefix in prefixes:
            candidate = prefix + root
            for word in cluster:
                if candidate in word:
                    if candidate not in prefixed_roots:
                        prefixed_roots[candidate] = set()
                    prefixed_roots[candidate].add(word)
        return prefixed_roots

    # create a graph of lexemes and cluster it according to
    # the alternative forms defined above

    lexeme_graph: Dict[str, set] = dict() # key = lexeme, value = set(lexemes)
    
    for lexeme in lexemes:
        forms = find_alternative_forms(lexeme)
        lexeme_graph[lexeme] = forms

    for lexeme in lexemes:
        cluster = lexeme_graph[lexeme]
        for child in list(cluster):
            cluster.update(lexeme_graph[child])
            lexeme_graph[child] = cluster

    # remove small clusters (4 and smaller)
    # this removes most noise that is not verbs
    small_lexemes = set(l for l in lexemes if len(lexeme_graph[l]) <= 4)
    for l in small_lexemes:
        del lexeme_graph[l]

    # rearrange clusters by their roots
    clusters = dict()
    for lexeme in lexeme_graph:
        root = find_cluster_root(lexeme_graph[lexeme])
        clusters[root] = lexeme_graph[lexeme]

    # extract prefixed verbs from clusters
    prefixed_clusters = dict()
    for root, cluster in clusters.items():
        pruned_cluster = set(cluster)
        for prefixed_root, sub_cluster in find_prefixed_roots(root, cluster).items():
            prefixed_clusters[prefixed_root] = sub_cluster
            pruned_cluster.difference_update(sub_cluster)
        prefixed_clusters[root] = pruned_cluster

    # convert to infinitives with lexemes and return
    infinitives = {
        root + "en": set(cluster)
        for root, cluster in prefixed_clusters.items()
    }

    # debug print result
    # for inf, cluster in sorted(infinitives.items(), key=lambda x: x[0]):
    #     #print(inf, end=" ")
    #     print(inf, cluster)
    # print()
    # print(len(prefixed_clusters))

    return infinitives
