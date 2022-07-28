import os
import re
import logging
from flask import Flask
from flask.helpers import make_response
from flask_cors import CORS
from tashaphyne.stemming import ArabicLightStemmer
from root_dictionary import RootDictionary
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "https://sarf.one"], methods=["GET"])
app.config['JSON_AS_ASCII'] = False
root_dictionary = RootDictionary('data/word-root-table.txt')
@app.route('/root-ext/<word>')
def index(word):
    logging.info("Request for word: %s", word)
    if not word:
        return make_response('ينبغي إرسال كلمة لإستخراج جذرها.', 400)

    word = word.strip()
    if len(word) > 50:
        return make_response('الكلمة لا تبدو صحيحة', 400)
    
    roots = extract_root(word)
    logging.info("Roots: %s", roots)
    if not roots:
        return make_response(f'لم يستطع البرنامج إستخراج جذر من {word}', 404)

    result = {word: list(roots)}
    return result

def extract_root(word) -> set:
    if not word:
        return None
    try:
        #Step 0: use the word as is
        roots = find_roots(word)
        if len(roots) > 0:
            return roots

        #Step 1: normalize the word then use as is
        word_normalized = normalize_word(word)
        if word_normalized != word:
            logging.info("Normalized word: %s", word_normalized)
            roots = find_roots(word_normalized)
            if len(roots) > 0:
                return roots
        
        #Step 2: use a light stemmer to get root, then look it up.
        lightStemmer = ArabicLightStemmer()
        lightStemmer.light_stem(word)
        possible_root = lightStemmer.get_root()
        if not possible_root:
            logging.info("Could not get root from stemmer for %s", word)
            return set()

        if possible_root != word_normalized:
            logging.info("Possible root: %s", possible_root)
            roots = find_roots(possible_root)
            return roots

        return set()
    except Exception as ex:
        logging.error(ex)

    return ""


def find_roots(word) -> set:
    """
    Prefer exact spelling, if not use alternate spellings
    """
    roots = get_all_possible_roots(word)
    if len(roots) > 0:
        return roots

    alt_spellings = permute_alternate_spelling(word)
    logging.info("Alternate spellings: %s", alt_spellings)
    roots = set()
    for alt_spelling in alt_spellings:
        roots = roots.union(get_all_possible_roots(alt_spelling))
    if len(roots) > 0:
        return roots
    return set()

def normalize_word(word) -> str:
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

def get_all_possible_roots(word) -> set:
    if not word:
        return set()
    return root_dictionary.get_all_possible_roots(word)

def permute_alternate_spelling(word) -> set:
    if not word:
        return set()
    alef_table = [u'أ', u'إ', u'آ', u'ا']
    hamza_table = [u'ؤ', u'ئ', u'ء']
    yaa_table = [u'ي', u'ى']

    words = [""]
    for char in word:
        alt_spellings = [char]
        if char in alef_table:
            alt_spellings = alef_table
        elif char in hamza_table:
            alt_spellings = hamza_table
        elif char in yaa_table:
            alt_spellings = yaa_table

        new_words = []
        for existing_word in words:
            for alt_spelling in alt_spellings:
                new_words.append(existing_word + alt_spelling)
        words = new_words
        if len(words) >= 100 :
            break

    return set(words)

if __name__ == '__main__':
    logging.info('Starting server...')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
    logging.warning('done.')