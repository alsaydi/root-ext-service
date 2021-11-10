import sys
from os import system
import logging

class RootDictionary:
    WORD_ROOT_SEPARATOR = '#'
    def __init__(self, file_name):
        logging.info('Initializing dictionary from file: %s', file_name)
        self.file_name = file_name
        self.lines = self.__read_file__()
        self.word_root_dictionary = self.__build_word_root_dictionary__()
        self.roots = self.word_root_dictionary.values()

    def get_all_possible_roots(self, word):
        result_set = set()
        if word in self.word_root_dictionary:
           result_set = self.word_root_dictionary[word]

        if word in self.roots:
            result_set.add(word)

        if len(result_set) == 0:
            logging.info('No roots found for word: %s ', word)
        return result_set

    def __read_file__(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines
        except Exception as ex:
            print(ex, file=system.stderr)
        return []

    def __build_word_root_dictionary__(self):
        word_root_dictionary = {}
        for line in self.lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(self.WORD_ROOT_SEPARATOR)
            if len(parts) != 2:
                continue
            word = parts[0]
            root = parts[1]
            if word in word_root_dictionary:
                word_root_dictionary[word].add(root)
            else:
                word_root_dictionary[word] = set([root])
        return word_root_dictionary

if __name__ == '__main__':
    print('This is a module for building a dictionary of word roots.')