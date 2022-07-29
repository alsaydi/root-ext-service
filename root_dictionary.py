from os import system
import logging

class RootDictionary:
    WORD_ROOT_SEPARATOR = '#'
    MULTI_ROOT_SEPARATOR = ","
    def __init__(self, file_name):
        logging.info('Initializing dictionary from file: %s', file_name)
        self.word_root_dictionary = self.__build_word_root_dictionary__(file_name)
        self.roots = self.word_root_dictionary.values()

    def get_all_possible_roots(self, word) -> set:
        result_set = set()
        if word in self.word_root_dictionary:
           result_set = self.word_root_dictionary[word]

        if word in self.roots:
            result_set.add(word)

        if len(result_set) == 0:
            logging.info('No root found for word: %s ', word)
        return result_set

    def __build_word_root_dictionary__(self, file_name) -> dict:
        word_root_dictionary = {}
        with open(file_name, mode='r') as dict_file:
            line = dict_file.readline()
            while line:
                line = line.strip()
                parts = line.split(self.WORD_ROOT_SEPARATOR)
                word = parts[0]
                root = parts[1]
                if word in word_root_dictionary:
                    word_root_dictionary[word].add(root)
                else:
                    word_root_dictionary[word] = set(filter(None,root.split(self.MULTI_ROOT_SEPARATOR)))
                line = dict_file.readline()
        return word_root_dictionary

if __name__ == '__main__':
    print('This is a module for building a dictionary of word roots.')