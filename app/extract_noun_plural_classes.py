from typing import Set


def contains_umlaut(word: str) -> bool:
    lword = word.lower()
    return ("ä" in lword) or ("ë" in lword) or ("ï" in lword) \
        or ("ö" in lword) or ("ü" in lword)


def remove_last_umlaut(word: str) -> str:
    tr = {
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
        "Ä": "A", "Ë": "E", "Ï": "I", "Ö": "O", "Ü": "U",
    }
    for i in range(len(word) - 1, 0, -1):
        if contains_umlaut(word[i]):
            return word[:i] + tr[word[i]] + word[i+1:]


def extract_noun_plural_classes(tagged_words: Set[str]):
    #
    # declension classes can be found at:
    # https://en.wikipedia.org/wiki/German_nouns
    #
    # best way to check declension of individual words is to find them at:
    # https://www.verbformen.com/
    #

    tagged_nouns = set(w for w in tagged_words if "NOUN" in w)

    #NMberg = set() # ignore: indistiguishable from "Lehrling"
    NMstaat = set()
    NMfahrer = set()
    NMlehrling = set()
    NMstudent = set()
    NMname = set()
    NMall = set(w.split("\t")[0] for w in tagged_nouns if "Gender=Masc" in w)
    NMall_sing_nom_acc_dat = set(
        w.split("\t")[0] for w in tagged_nouns
        if "Gender=Masc" in w and "Number=Sing" in w and "Case=Gen" not in w
    )
    NMall_sing_acc_dat = set(
        w.split("\t")[0] for w in tagged_nouns
        if "Gender=Masc" in w and "Number=Sing" in w and (
            ("Case=Acc" in w) or ("Case=Dat" in w)
        )
    )

    NFmutter = set()
    NFmeinung = set()
    NFkraft = set()
    NFkamera = set()
    NFall = set(w.split("\t")[0] for w in tagged_nouns if "Gender=Fem" in w)

    NNbild = set()
    NNradio = set()

    def categorize_masculine_word(word, tags):
        # singular genitive for Student and Name classes
        # have unusual suffixes we can leverage
        if "Number=Sing" in tags:
            if "Case=Gen" in tags:
                if word[-2:] == "en":
                    if word[:-2] in NMall:
                        NMstudent.add(word[:-2])
                    elif word[:-1] in NMall:
                        NMstudent.add(word[:-1])
                if word[-2:] == "ns":
                    if word[:-2] in NMall:
                        NMname.add(word[:-2])

        # Otherwise we check the suffixes in plural (they're the same
        # for all cases within each class, except for dative so we skip
        # dative) and then we try to find the same word with or without
        # the suffix in singular (in two different unions of singular cases)
        if "Number=Plur" in tags:
            if "Case=Dat" not in tags:
                if word[-2:] == "en":
                    if word[:-2] in NMall_sing_acc_dat:
                        NMstaat.add(word[:-2])
                    if word in NMall_sing_acc_dat:
                        NMstudent.add(word[:-2])
                        pass
                elif word[-1:] == "e":
                    if word[:-1] in NMall_sing_nom_acc_dat:
                        NMlehrling.add(word[:-1])
                else:
                    if word in NMall_sing_nom_acc_dat:
                        NMfahrer.add(word)

    def categorize_feminine_word(word, tags):
        # focus only on plural, since singular feminine nouns do not flex at all
        if "Number=Plur" not in tags:
            return

        # only Kamera class has "s" suffix in all cases
        if word[-1:] == "s":
            NFkamera.add(word[:-1])
            return

        # suffix "-en" (or "-e" after "r" and "l") is in most cases
        # indicative of the class Meinung. In the dative case,
        # the suffix can also indicate Kraft class.
        # We desambiguate based on umlauts.
        elif word[-2:] in ["en", "rn", "ln"]: # Tafelen -> Tafeln : E-Deletion after "r" and "l"
            root = word[:-2] if word[-2:] == "en" else word[:-1]
            if "Case=Dat" not in tags:
                NFmeinung.add(root)
                return
            else: # desambiguate kraft and meinung
                if not contains_umlaut(word):
                    NFmeinung.add(root)
                    return
                if remove_last_umlaut(root) in NFall:
                    NFkraft.add(remove_last_umlaut(root))
                    return

        # Suffix "-e" in non-datives case uniquely identifies class Kraft
        elif word[-1:] == "e":
            if "Case=Dat" not in tags:
                NFkraft.add(word[:-1])
                return

        # No suffix and added umlaut in non-dative cases uniquely
        # identifies the Mutter class
        elif remove_last_umlaut(word) in NFall:
            if "Case=Dat" not in tags:
                NFmutter.add(remove_last_umlaut(word))

    def categorize_neuter_word(word, tags):
        # focus only on plural, since singular neuter nouns flex all in the same way
        if "Number=Plur" not in tags:
            return
            
        # Suffix "-s" in all cases indicates the Radio class
        if word[-1:] == "s":
            NNradio.add(word[:-1])
            return

        # Suffix "-er" or "-ern" indicates the Bild class
        elif "Case=Dat" not in tags and word[-2:] == "er":
            NNbild.add(word[:-2])
            return
        elif "Case=Dat" in tags and word[-3:] == "ern":
            NNbild.add(word[:-3])
            return

    # categorize all words
    for w in tagged_nouns:
        word, tags = w.split("\t")
        if "Gender=Masc" in tags:
            categorize_masculine_word(word, tags)
        elif "Gender=Fem" in tags:
            categorize_feminine_word(word, tags)
        elif "Gender=Neut" in tags:
            categorize_neuter_word(word, tags)

    return {
        "NMstaat": NMstaat,
        "NMfahrer": NMfahrer,
        "NMlehrling": NMlehrling,
        "NMstudent": NMstudent,
        "NMname": NMname,
        
        "NFmutter": NFmutter,
        "NFmeinung": NFmeinung,
        "NFkraft": NFkraft,
        "NFkamera": NFkamera,
        
        "NNbild": NNbild,
        "NNradio": NNradio,
    }
    
    # Idea for possible improvement:
    # create a map of compound words (by finding suffix of X in Y and
    # declaring Y to be a compound of X) Compounds have the same
    # declension class as the original word.