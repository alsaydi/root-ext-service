import os
import re
import sys
from flask import Flask
from flask.helpers import make_response
from tashaphyne.stemming import ArabicLightStemmer
from root_dictionary import RootDictionary

app = Flask(__name__)
root_dictionary = RootDictionary('data/word-root-table.txt')
@app.route('/<word>')
def index(word):
    if not word:
        return make_response('ينبغي إرسال كلمة لإستخراج جذرها.', 400)

    roots = extract_root(word)
    if not roots:
        return make_response(f'لم يستطع البرنامج إستخراج جذر من {word}', 404)

    result = {word: list(roots)}
    return result

def extract_root(word):
    if not word:
        return None
    try:
        word = normalize_word(word)
        lightStemmer = ArabicLightStemmer()
        lightStemmer.light_stem(word)
        possible_root = lightStemmer.extract_root()
        if possible_root is None or len(possible_root) == 0:
            possible_root = word
        roots = get_all_possible_roots(possible_root)
        return roots
    except Exception as ex:
        print(ex, file=sys.stderr)

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
        print(ex, file=sys.stderr)

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
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))