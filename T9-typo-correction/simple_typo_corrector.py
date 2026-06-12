import pandas as pd
from difflib import get_close_matches

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 100)


df = pd.read_csv('data/t9_advanced_typo_correction_dataset.csv')
correct_words = df['correct_word'].unique().tolist()

def suggest_correction(word, candidates = correct_words, n = 5, cutoff = 0.7):
    return get_close_matches(word, candidates, n = n, cutoff = cutoff)

def correct_sentence(sentence, candidates = correct_words):
    words = sentence.split()
    corrected_words = []
    for w in words:
        suggestions = suggest_correction(w, candidates)
        if suggestions:
            corrected_words.append(suggestions[0])
        else:
            corrected_words.append(w)
    return ' '.join(corrected_words)

sentence = 'I am lerning pythom with hella fun'
print('Original:', sentence)
print('Corrected:', correct_sentence(sentence))