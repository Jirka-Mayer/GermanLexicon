Homework - German Lexicon
=========================

- **Course:** [Morphological and Syntactic Analysis](https://ufal.mff.cuni.cz/courses/npfl094)
- **Assignment:** [here](https://ufal.mff.cuni.cz/~zeman/vyuka/morfosynt/lab-lexicon/index.html)


Setup & Execution
-----------------

1. Download the german corpus and put into the `data` folder:
    - `wget -O data/de-tagged.txt.gz https://ufal.mff.cuni.cz/~zeman/vyuka/morfosynt/lab-lexicon/de-tagged.txt.gz`
2. Execute `main.py` to extract the lexicon
    - `python3 main.py`
3. Read the program output for rough overview and see the output files in the `data` folder


Implemented Extraction Process
------------------------------

Closed class words (articles, pronouns, prepositions, conjunctions) are enumerated in file [`app/closed_classes.py`](app/closed_classes.py) and for the open class words we are primarily interested in nouns, adjectives, verbs and adverbs.


### Verbs

- non-weak verbs?

- verbs
    - not capitalized
    - infinitive ends with -en
        - kauf-en
        - kauf-e
        - kauf-st !! <-- only weak verbs do this
        - ge-kauf-t !! <-- only weak verbs do this


### Nouns

- nouns
    - capitalized in the middle of a sentence
    - determine
        - gender
        - plural class
        - https://www.thegermanproject.com/german-lessons/nouns
        - https://en.wikipedia.org/wiki/German_nouns


### Adjectives

- adjectives
    - not capitalized
    - atributive adjectives
        - precede nouns directly -> we can use that
        - end with "-e", "-en"
            - https://en.wikipedia.org/wiki/German_declension#Attributive_adjectives
    - comparative & superlative declensions can be used!
        - http://germanforenglishspeakers.com/adjectives/comparative-and-superlative-forms/


### Adverbs

- adverbs
    - same words as adjectives, only without suffix "-e", "-en"
    - german calls them Eigenschaftswörter (property words)
        - https://en.wikipedia.org/wiki/Adjective#Adverbs
    - there are words that act as adverbs, but are not adjectives
        - http://germanforenglishspeakers.com/other/adverbs/
        - are they really? They seem to be usable as adverbs.
