import pandas as pd
import Levenshtein

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 100)

df = pd.read_csv('data/t9_typo_correction_dataset.csv')
correct_words = df['correct_word'].unique().tolist()

def calculate_score(typo_word, candidate_word):
    score = 0
    if typo_word[0] == candidate_word[0]:
        score += 2

    if typo_word[-1] == candidate_word[-1]:
        score += 2

    distance = Levenshtein.distance(typo_word, candidate_word)
    score += max(0, 10 - distance)

    length_diff = abs(len(typo_word) - len(candidate_word))
    score += max(0, 2 - length_diff)

    return score

def suggest_correction(typo_word, candidate_words, top_n = 3):
    candidates = [cw for cw in candidate_words if cw[0] == typo_word[0] and Levenshtein.distance(typo_word, cw) <= 2]
    scored_candidates = [(cw, calculate_score(typo_word, cw)) for cw in candidates]
    scored_candidates.sort(key = lambda x: x[1], reverse = True)
    return scored_candidates[:top_n]

def correct_sentence(sentence, candidate_words):
    words = sentence.split()
    corrected_words = []
    for w in words:
        word = w.lower()
        if len(word) <= 2:
            corrected_words.append(w)
            continue
        if word in candidate_words:
            corrected_words.append(w)
            continue

        suggestions = suggest_correction(word, candidate_words)
        if suggestions:
            best_word, best_score = suggestions[0]
            corrected_words.append(best_word)
        else:
            corrected_words.append(w)
    return ' '.join(corrected_words)

test_sentence = 'I am lerning pythom with hella fun'
corrected_sentence = correct_sentence(test_sentence, correct_words)
print('Original:', test_sentence)
print('Corrected:', corrected_sentence)