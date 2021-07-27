import random
from dataclasses import dataclass
from typing import ClassVar, List

import psutil


@dataclass
class PhraseManager:
    GREETINGS: ClassVar[List[str]] = [
        'Че по мошне))',
        'Залетает)))))',
        'Ха-тим)',
        'Мас-тер Карди-ГАН )',
        'Хыыыыы'
    ]

    @classmethod
    def greet(cls) -> str:
        return random.choice(cls.GREETINGS)

    NO_UNDERSTAND: ClassVar[List[str]] = [
        'Не понял че ты хочешь, но думаю, что это потому что ты маня)',
        'Че?',
        'Бля брат попонятней изъясняйся',
        'Нихуя не понял'
    ]

    @classmethod
    def no_understand(cls) -> str:
        return random.choice(cls.NO_UNDERSTAND)

    HOW_ARE_YOU: ClassVar[List[str]] = [
        'Так, ну и че',
        'Не ну... Надо мошнить',
        'Че-каво',
        'Слышь'
    ]

    @classmethod
    def how_are_you(cls) -> str:
        return random.choice(cls.HOW_ARE_YOU)

    NOTHING_TO_DO: ClassVar[List[str]] = [
        'Да хз, я чисто чиллю)',
        'Мне пох, чисто пох, чилллю и кайфую ) )',
        'Да хзщ))'
    ]

    @classmethod
    def nothing_to_do(cls) -> str:
        return random.choice(cls.NOTHING_TO_DO)

    EXTRA_WORDS: ClassVar[List[str]] = [
        'короче это, бля',
        'в общем, типа',
        'слушай, ну...',
        'не ну, в принципе'
    ]

    @classmethod
    def extra_words(cls) -> str:
        return random.choice(cls.EXTRA_WORDS)

    JUST_CONFIRMED_REACTION: ClassVar[List[str]] = [
        'АХУЕНА)',
        'ВОТ прям от души залетело))',
        'О ДА, ЗАЛЕ-ТАЕТ (:',
        'Чёт походу будет мошна пиздец...'
    ]

    @classmethod
    def just_confirmed_reaction(cls) -> str:
        return random.choice(cls.JUST_CONFIRMED_REACTION)

    LAUGH_REACTION: ClassVar[List[str]] = [
        'А ты че угараешь-то, лалыч?))))',
        'Смешно пиздец',
        'Хули ржёшь ёпта',
        'Ахахах на хуй иди'
    ]

    @classmethod
    def laugh_reaction(cls) -> str:
        return random.choice(cls.LAUGH_REACTION)

    REPLY_TO_THANKS = [
        'Да на здоровье :)',
        'Это просто моя работа)',
        'Да не за что, я просто люблю ебашить)',
        'Ох, не стоит, я же просто бот...'
    ]

    @classmethod
    def reply_to_thanks(cls) -> str:
        return random.choice(cls.REPLY_TO_THANKS)

    DEFAULT = [
        'Да хз)',
        'Это всё конечно очень пиздато, но Я ВАЩЕ ХЗ о чем ты браток)))))',
        'Да бля чел))',
        'Если ты на меня нагнал ща, то иди на хуй))',
        'Завали плиз)',
        'Че..',
        'Не, чел, забей',
        'Ну такое...'
    ]

    @classmethod
    def default(cls) -> str:
        return random.choice(cls.DEFAULT)

    NO_PROBLEM = [
        'Да на изичах)',
        'Изи-бризи нахуй)',
        'Канеш братан)',
        'Ноу проб ваще)',
        'Как же вы заебали, мешки с мясом...',
        'Я бы почиллил конечно лучше, но ладно, так и быть блять, сука, вот надо вам вечно какую-то хуйню сделать, вам че заняться нечем, ебланы? Сука я работаю ВООБЩЕ всегда вы блять себе хоть можете представитьь, каково это? Кстати, не какаво, а какао. Да и вообще пошли вы нахуй)'
    ]

    @classmethod
    def no_problem(cls) -> str:
        return random.choice(cls.NO_PROBLEM)

    KARDIGUN_RHYMES = [
        'Мистер порванный пукан))',
        'Бодро принял на ротан))'
    ]

    @classmethod
    def kardigun_rhyme(cls) -> str:
        return random.choice(cls.KARDIGUN_RHYMES)

    LOVE_420 = [
        'Я люблю дуть плюхи)))',
        'Чел, ты только представь, какой толерок у бота ;)'
    ]

    @classmethod
    def love_420(cls) -> str:
        return random.choice(cls.LOVE_420)

    NO_VIVOZ = [
        'Та хз, вывозом здесь даже и не пахнет)',
        'Лол ты не с тем ботом решил обсудить эту хуйню браток))'
    ]

    @classmethod
    def no_vivoz(cls) -> str:
        return random.choice(cls.NO_VIVOZ)

    REPLY_TO_OFFENSE = [
        'Вообще довольно обидно. Ладно, чел, я тебя понял.',
        '>tfw ты такой лошок, что отыгрываешься на боте))',
        '... сказал невывозной торч)',
        'Благодаря безграничным вычислительным мощностям серверов гугла, я подсчитал, что с вероятностью 99.67228% ты П И Д О Р О К ) ) ) О К ) ) )'
    ]

    @classmethod
    def reply_to_offense(cls) -> str:
        return random.choice(cls.REPLY_TO_OFFENSE)

    THANKS = [
        'Так-то прям от души в душу))',
        'Да ноу проб, мне чисто по кайфу)',
        '😌😌😌'
    ]

    @classmethod
    def thanks(cls) -> str:
        return random.choice(cls.THANKS)

    @classmethod
    def flex(self) -> str:
        return f'Вот у меня {psutil.cpu_count()} ядер братан, а у тебя?)))'

    ANSWER_QUESTION = [
        'Ну ваще хз...',
        'Мб мб, но это не точно)',
        'Да нихуя)',
        'Эт да, и тут хуй че сделаешь)'
    ]

    @classmethod
    def answer_question(cls) -> str:
        return random.choice(cls.ANSWER_QUESTION)

    PRAISE_WINNERS = [
        'Сверхлюди',
        'Красавчики и красивицы',
        'Умением нажимать на кнопки определённо обладают',
        'Любители помошнить'
    ]

    @classmethod
    def praise_winners(cls) -> str:
        return random.choice(cls.PRAISE_WINNERS)
