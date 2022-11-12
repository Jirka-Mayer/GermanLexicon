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

I chose to use German. The German corpus used contains POS tags already, but I decided to ignore them and try to determine these tags myself.

Closed class words (articles, pronouns, prepositions, conjunctions) are enumerated in file [`app/closed_classes.py`](app/closed_classes.py) and for the open class words we are primarily interested in nouns, adjectives, verbs and adverbs.


### Verbs

There are [five categories of verbs](http://germanforenglishspeakers.com/verbs/verb-types/) in German, where only the weak-verb category could be considered an open class. These verbs have a given inflection pattern we can leverage to detect them. For example with the verb `einkaufen` (to go shopping), we can get the following forms:

```
ein-kauf-en
kauf
kauf-e      ein
kauf-en     ein
kauf-t      ein
kauf-te     ein
kauf-st     ein
ein-ge-kauf-t
```

The morpheme `ein` is a separable prefix and these can be listed and accounted for:

```
zurück nach auf aus bei ein los mit hin her vor weg an ab zu
```

For a given lexeme (say `einkaufte`) we can generate possible roots (`kaufte`, `kauft`, `kauf`) and add prefixes and suffixes to them to list potential other lexems. We search for those and create a set of other, related lexemes. We then cluster the lexemes by this condition creating lexeme groups and we select a root-word for each such group. We also remove groups that have too little lexemes. Finally, we try to separate different forms of the same verb with different separable prefixes to get all the possible verb infinitives and their corresponding found lexemes.

The result is printed into the file `data/lexicon-weak-verbs.txt.gz` in the form:

```
{infinitive} {tab} {lexeme1} {space} {lexeme2} ... {\n}
-----------------------------------------------------------------------------
ausgefallen     ausgefallen ausgefallene ausgefallenen
ausgeflogen     ausgeflogen
ausgefunden     herausgefunden
ausgegangen     ausgegangen vorausgegangen vorausgegangene vorausgegangenen
ausgegeben      ausgegeben herausgegeben
ausgehenden     ausgehend ausgehende ausgehenden hinausgehende hinausgehenden
ausgekommen     herausgekommen hinausgekommen
ausgeladen      ausgeladen
ausgelassen     ausgelassen
ausgelaufen     ausgelaufen
ausgenommen     ausgenommen herausgenommen
```


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

In German, most adverbs are formed by placing an adjective next to a verb and removing the inflexion suffix used for adjectives (-e, -en). Therefore the lexicon of adjectives can be used to model adverbs in places where the semantics makes sense. In German, both adjectives and adverbs are called [Eigenschaftswörter (property words)](https://en.wikipedia.org/wiki/Adjective#Adverbs), forming a single category.

There are only a handful of words that act as adverbs and not as adjectives. Listing the unique words in the given tagged corpus we get the following numbers:

- 75 722 unique words in total
- 18 639 unique adjectives
- 355 unique adverbs

For this reason I decided not to extract adverbs automatically, since they can be listed manually.

[More info on adverbs](http://germanforenglishspeakers.com/other/adverbs/).
