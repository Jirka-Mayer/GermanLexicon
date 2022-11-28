from typing import List
from app.closed_classes import *


class NounAdjectiveProcessor:
    def __init__(self, words: List[str]):
        self.words: List[str] = words

        self.nouns = []
        self.multiword_proper_nouns = []
        self.multiword_proper_nouns_sliced = []
        self.adjectives = []
    
    def run(self):
        for i, word in enumerate(self.words):
            if word[0].isupper():
                self.process_capitalized_word(word, i)
    
    def process_capitalized_word(self, word: str, index: int):
        if index == 0: return
        predecessor = self.words[index - 1]

        # all words at the start of a sequence are capitalized,
        # they are not useful
        if self.is_start_of_sentence(index):
            return

        # if the predecessor is not an alphabetical word, it's probbably some
        # mess that we are not interested in
        if not predecessor.isalpha():
            return
        
        # two capitalized words in succession
        # => this is probbably a multi-word proper noun
        if predecessor[0].isupper():
            self.process_multiword_proper_noun(index)
            return

        # now we have one non-capitalized word and one capitalized in isolation

        # the capitalized word is a noun, definitely,
        # maybe a proper noun, it doesn't matter
        self.nouns.append(word)

        # the non-capitalized word may or may not be an adjective
        
        # filter out closed classes
        if is_closed_class(predecessor):
            return

        # TODO: numerals and modal verbs come through here sometimes
        self.adjectives.append(predecessor)
        # print(predecessor, word)

    def process_multiword_proper_noun(self, index):
        # get the start and end indices of a capitalized word sequence
        start = index
        end = index
        while start >= 0 and self.words[start][0].isupper():
            start -= 1
        while end < len(self.words) and self.words[end][0].isupper():
            end += 1
        start += 1
        end -= 1

        # we will be called on every subword, only trigger on the last subword
        # to not report this sequence multiple times
        if index != end:
            return

        # if the first word is start of a sentence, we don't know whether
        # it is or is not included. Ignore the whole multiword then.
        if self.is_start_of_sentence(start):
            return

        # get the multi-word proper noun
        proper_noun = " ".join(self.words[start:end+1])
        self.multiword_proper_nouns.append(proper_noun)
        self.multiword_proper_nouns_sliced += self.words[start:end+1]
        # print(proper_noun)

    def is_start_of_sentence(self, index: int) -> bool:
        if index == 0: return
        predecessor = self.words[index - 1]
        
        if predecessor[0].isalpha():
            return False

        if predecessor[0].isdigit():
            return False

        if predecessor in [
            ",", "-", ";", "/", "(", ")", "%", "+", "'s", "'"
        ]: return False

        if predecessor in [".", "``", "''", "?", "!", ":", "..."]:
            return True

        # .com .de -something
        if predecessor[0] in ["-", "."]:
            return False
        
        # random mess that remains
        return False
        #print(predecessor, self.words[index])
