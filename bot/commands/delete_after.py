from typing import List, Optional


def get_delete_after(tokens: List[str]) -> Optional[str]:
    option = list(filter(lambda token: token.startswith('$') and token[-1] in 'smhd', tokens))
    return option[0] if len(option) > 0 else None
