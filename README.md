Homework - German Lexicon
=========================

- **Course:** [Morphological and Syntactic Analysis](https://ufal.mff.cuni.cz/courses/npfl094)
- **Lexicon Assignment:** [here](https://ufal.mff.cuni.cz/~zeman/vyuka/morfosynt/lab-lexicon/index.html)
- **Two-level Morphology Assignment:** [here](https://ufal.mff.cuni.cz/~zeman/vyuka/morfosynt/lab-twolm/index.html)


Setup & Execution
-----------------

1. Download the german corpus and put into the `data` folder:
    - `wget -O data/de-tagged.txt.gz https://ufal.mff.cuni.cz/~zeman/vyuka/morfosynt/lab-lexicon/de-tagged.txt.gz`
2. Execute build script to prepare necessary files
    - `bash build.sh`
3. See the output files in the `data` folder
    - `lexicon-*` files are lexicons extracted without using POS tags, only the verbs are used for morpological analysis
    - `german_*` files are for the morphological analysis, the verb lexicon contains inflection classes extracted from words known to be nouns thanks to the POS tags
4. Feed the example input file through the analyzer
    - `bash analyze.sh < example.txt`


Implemented Extraction Process
------------------------------

I chose to use German. The German corpus contains POS tags already, but I decided to ignore them and try to determine these tags myself. I managed to extract nouns, verbs and adjectives. These can be browsed in the `data` folder:

```
### data/lexicon-nouns.txt.gz ###
Altfall-Regelung
Altfallregelung
Altfälle
Altgeräte
Altgesellschafter
Altkredite
Altlasten
Altlasten-Probleme
Altlastensanierung
```

```
### data/lexicon-adjectives.txt.gz ###
alternativer
alternde
alternden
alterndes
alternierender
altersbedingte
altersbedingten
altes
```

```
### data/lexicon-weak-verbs.txt.gz ###
angeschlagen    angeschlagen angeschlagene angeschlagenen
angeschlossen   angeschlossen angeschlossene angeschlossenen
angeschoben     angeschoben
angeschrieben   angeschrieben
angesehen       angesehen angesehene angesehenen
angesprochen    angesprochen angesprochene angesprochenen
```

For the morphological analysis I realized I need to extract inflection classes of nouns, as they are the most interesting feature of German in this regard. I decided to use the POS tags so that I at least work with the true set of all nouns.

These noun classes together with the weak verbs are used to create a morpological analyzer using `foma`.


Extraction of Open Classes Without POS Tags
-------------------------------------------

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

Nouns are extracted by taking words that are capitalized in the middle of a sentence. This means we don't get nouns at the beginning of a sentence, but that is not such a problem. We cannot take all capitalized words as-is, because proper nouns may have multiple words and it is therefore incorrect to mark each of their sub-words as a standalone noun (e.g. `Präsidenten George Bush`).


### Adjectives

Adjectives are extracted by taking the non-capitalized words that immediately precede nouns. These words are mostly articles (`der`, `ein`) or pronouns (`mir`, `diese`) or other closed classes that can be enumerated and filtered out. What remains are mostly adjectives, with a few numerals in between (numerals often behave like adjectives).


### Adverbs

In German, most adverbs are formed by placing an adjective next to a verb and removing the inflexion suffix used for adjectives (-e, -en). Therefore the lexicon of adjectives can be used to model adverbs in places where the semantics makes sense. In German, both adjectives and adverbs are called [Eigenschaftswörter (property words)](https://en.wikipedia.org/wiki/Adjective#Adverbs), forming a single category.

There are only a handful of words that act as adverbs and not as adjectives. Listing the unique words in the given tagged corpus we get the following numbers:

- 75 722 unique words in total
- 18 639 unique adjectives
- 355 unique adverbs

For this reason I decided not to extract adverbs automatically, since they can be listed manually.

[More info on adverbs](http://germanforenglishspeakers.com/other/adverbs/).


TODO: extraction of noun classes
TODO: setup of morpho analysis (document used tags)