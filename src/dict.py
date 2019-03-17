import json
import difflib
from src.util import is_kana

def init_dict():
        smk_dict = []
        for i in range(1, 10):
                f = open(f'./shinmeikai/term_bank_{i}.json')
                smk_dict += json.load(f)
                f.close()
        return smk_dict

def dict_search(search_q, smk_dict, limit=25):
        matches = []
        if is_kana(search_q):
                matches = [m for m in ((difflib.SequenceMatcher(a = w[1], b = search_q).ratio(), w) for w in smk_dict) if m[0] > 0.7]
        else:
                matches = [m for m in ((difflib.SequenceMatcher(a = w[0], b = search_q).ratio(), w) for w in smk_dict) if m[0] > 0.3]
        return format_results([m[1] for m in sorted(matches, key=lambda m: m[0], reverse=True)[:limit]])

def format_results(matches):
        return [(m[0], m[1], m[5]) for m in matches]