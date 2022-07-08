def is_alpha(c: str) -> bool:
    return '0' <= c <= '9' \
           or 'a' <= c <= 'z' \
           or 'A' <= c <= 'Z' \
           or 'а' <= c <= 'я' \
           or 'А' <= c <= 'Я'


def get_alpha_part(s: str) -> str:
    for i, c in enumerate(s, 0):
        if not is_alpha(c):
            return s[:i]
    return s
