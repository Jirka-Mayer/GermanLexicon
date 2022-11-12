################################################################################
# Articles                                                                     #
################################################################################

ARTICLES = set({
    "der", "des", "dem", "den", # masculine
    "die", "der", "der", "die", # feminine
    "das", "des", "dem", "das", # neuter
    "die", "die", "den", "der", # plural

    # ein
    "ein", "eine", "einer", "eines", "einem", "einen",
})

def is_article(word: str):
    return word in ARTICLES


################################################################################
# Pronouns                                                                     #
################################################################################

# https://www.berlitz.com/blog/german-pronouns

def is_pronoun_subject(word: str) -> bool:
    return word.lower() in {
        "ich", "du", "er", "sie", "es",
        "wir", "ihr"
    }

def is_pronoun_direct_object(word: str) -> bool:
    return word.lower() in {
        "mich", "dich", "ihn", "sie", "es",
        "uns", "euch"
    }

def is_pronoun_indirect_object(word: str) -> bool:
    return word.lower() in {
        "mir", "dir", "ihm", "ihr",
        "uns", "euch", "ihnen"
    }

def is_pronoun_reflexive(word: str) -> bool:
    return word.lower() in {
        "mich", "dich", "sich",
        "uns", "euch"
    }

def is_pronoun_possesive(word: str) -> bool:
    return word.lower() in {
        "mein", "meine", "meiner", "meines", "meinen", "meinem",
        "dein", "deine", "deiner", "deines", "deinen", "deinem",
        "sein", "seine", "seiner", "seines", "seinen", "seinem",
        "ihr", "ihre", "ihrer", "ihres", "ihren", "ihrem",
        "unser", "unsere", "unserer", "unseres", "unseren", "unserem",
        "euer", "euere", "euerer", "eueres", "eueren", "euerem"
    }

def is_pronoun_relative(word: str) -> bool:
    return word.lower() in {
        # nominative
        "der", "die", "das",
        "welcher", "welche", "welches"

        # genitive
        "dessen", "deren",

        # dative
        "dem", "der", "denen",

        # accusative
        "den", "die", "das"
    }

def is_pronoun_indefinite(word: str) -> bool:
    return word.lower() in {
        "irgentjemand", "irgendwer",
        "man",
        "niemand",
        "kein", "keine", "keiner", "keines", "keinen", "keinem",
        "alle", "allen", "allem", "alles",
        "jede", "jeder", "jedes", "jeden", "jedem",
        "ander", "andere", "anderer", "anderes", "anderen", "anderem",
        "einig", "einige", "einiger", "einiges", "einigen", "einigem",
        "viel", "viele", "vieler", "vieles", "vielen", "vielem",
        "etliche",
        "etwas",
        "nichts",
        "irgendetwas"
    }

def is_pronoun_definite(word: str) -> bool:
    return word.lower() in {
        "dieser", "diese", "dieses", "diesen", "diesem",
        "der", "die", "das"
    }

def is_pronoun_interrogative(word: str) -> bool:
    return word.lower() in {
        "wie", "was", "wo", "wann", "warum", "wer", "wem", "wen", "wessen"
    }

def is_pronoun(word: str) -> bool:
    if is_pronoun_subject(word): return True
    if is_pronoun_direct_object(word): return True
    if is_pronoun_indirect_object(word): return True
    if is_pronoun_reflexive(word): return True
    if is_pronoun_possesive(word): return True
    if is_pronoun_relative(word): return True
    if is_pronoun_indefinite(word): return True
    if is_pronoun_definite(word): return True
    if is_pronoun_interrogative(word): return True
    return False


################################################################################
# Prepositions                                                                 #
################################################################################

def is_preposition(word: str):
    return word.lower() in {
        # accusative
        "bis",
        "durch",
        "entlang",
        "für",
        "gegen",
        "ohne",
        "um",
        
        # dative
        "aus",
        "bei", "beim",
        "mit",
        "nach",
        "von", "vom", "vor",
        "zu", "zum", "zur",
        "gegenüber",
        "seit",

        # mixed
        "an", "am",
        "auf",
        "hinter",
        "in", "im", "ins",
        "neben",
        "um",
        "unter",
        "über",
    }


################################################################################
# Conjunctions                                                                 #
################################################################################

def is_conjuntion(word: str):
    return word.lower() in {
        "und", "oder", "aber", "denn", "sondern",
        "doch", "jedoch", "beziehungsweise",

        "wenn", "bevor", "nachdem", "als",
        "bis", "weil", "falls", "dass", "daß",
    }


################################################################################
# All this stuff together                                                      #
################################################################################

def is_closed_class(word: str) -> bool:
    if is_article(word): return True
    if is_pronoun(word): return True
    if is_preposition(word): return True
    if is_conjuntion(word): return True
    return False
