import os
import re
import logging
from flask import Flask
from flask.helpers import make_response
from tashaphyne.stemming import ArabicLightStemmer
from root_dictionary import RootDictionary
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)

app = Flask(__name__)
root_dictionary = RootDictionary('data/word-root-table.txt')
@app.route('/<word>')
def index(word):
    logging.debug("Request for word: %s", word)
    if not word:
        return make_response('ينبغي إرسال كلمة لإستخراج جذرها.', 400)

    roots = extract_root(word)
    logging.debug("Roots: %s", roots)
    if not roots:
        return make_response(f'لم يستطع البرنامج إستخراج جذر من {word}', 404)

    result = {word: list(roots)}
    return result

def extract_root(word):
    if not word:
        return None
    try:
        word = normalize_word(word)
        logging.debug("Normalized word: %s", word)
        lightStemmer = ArabicLightStemmer()
        lightStemmer.light_stem(word)
        possible_root = lightStemmer.extract_root()
        if possible_root is None or len(possible_root) == 0:
            possible_root = word
        logging.debug("Possible root: %s", possible_root)
        alt_spellings = permute_alternate_spelling(possible_root)
        logging.debug("Alternate spellings: %s", alt_spellings)
        roots = set()
        for alt_spelling in alt_spellings:
            logging.debug("Extrating root from alternate spelling: %s", alt_spelling)
            spelling_roots = get_all_possible_roots(alt_spelling)
            logging.debug("Roots for spelling %s: %s",alt_spelling, spelling_roots)
            roots = roots.union(spelling_roots)
        return roots
    except Exception as ex:
        logging.error(ex)

    return ""

def normalize_word(word):
    if not word:
        return None
    try:
        # remove diacritics
        lightStemmer = ArabicLightStemmer()
        lightStemmer.light_stem(word)
        root = lightStemmer.get_unvocalized()
        regex = r'[ـًٌٍَُِّْٰ]'
        root = re.sub(regex, '', root)
        return root
    except Exception as ex:
        logging.error(ex)

def get_all_possible_roots(word):
    if not word:
        return []
    return root_dictionary.get_all_possible_roots(word)

def permute_alternate_spelling(word):
    if not word:
        return []
    aleft_table = [u'أ', u'إ', u'آ', u'ا']
    hamza_table = [u'ؤ', u'ئ', u'ء']
    yaa_table = [u'ي', u'ى']

    words = [""]
    for char in word:
        alt_spellings = [char]
        if char in aleft_table:
            alt_spellings = aleft_table
        elif char in hamza_table:
            alt_spellings = hamza_table
        elif char in yaa_table:
            alt_spellings = yaa_table

        new_words = []
        for existing_word in words:
            for alt_spelling in alt_spellings:
                new_words.append(existing_word + alt_spelling)
        words = new_words

    return words

if __name__ == '__main__':
    logging.info('Starting server...')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
    logging.warning('done.')