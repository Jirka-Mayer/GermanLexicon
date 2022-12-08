#!/bin/bash

# extract lexicons
python3 main.py

echo
echo "********************************"
echo

# concatenate the full lexicon
cat morpho/german_full_head.lexc \
    data/german_full_nouns.lexc \
    data/german_full_verbs.lexc \
> data/german_full.lexc

# build the analyzer
echo "\
source morpho/german_full.foma
save stack data/german_full.bin
" | foma
