class Emojis:
    RED_CROSS = '\u274c'
    GREEN_CHECK_MARK = '\u2705'
    SUNGLASSES = u'\U0001F60E'

    @classmethod
    def get_confirmation_status_emoji(cls, confirmed: bool) -> str:
        return cls.GREEN_CHECK_MARK if confirmed else cls.RED_CROSS
