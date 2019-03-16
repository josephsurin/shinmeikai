def is_kana(w):
        return all([12353 <= ord(c) <= 12439 or 12449 <= ord(c) <= 12542 for c in list(w)])