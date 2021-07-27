import random
from dataclasses import dataclass
from typing import ClassVar, List

import psutil


@dataclass
class PhraseManager:

    @classmethod
    def greet(cls) -> str:
        return random.choice([
            'Че по мошне))',
            'Залетает)))))',
            'Ха-тим)',
            'Мас-тер Карди-ГАН )',
            'Хыыыыы'
        ])

    @classmethod
    def no_understand(cls) -> str:
        return random.choice([
            'Не понял че ты хочешь, но думаю, что это потому что ты маня)',
            'Че?',
            'Бля брат попонятней изъясняйся',
            'Нихуя не понял'
        ])

    @classmethod
    def chel_response(cls) -> str:
        return random.choice([
            'Ммм?))',
            'Да-да?',
            'Че)',
            'бляяттб опять ты...',
            'Чел ты...'
        ])

    @classmethod
    def nice_call_response(cls) -> str:
        return random.choice([
            'Йо чел)',
            'Дарова, че каво?)',
            'че',
            'Что такое, братишка?'
        ])

    @classmethod
    def how_are_you(cls) -> str:
        return random.choice([
            'Так, ну и че',
            'Не ну... Надо мошнить',
            'Че-каво',
            'Слышь'
        ])

    @classmethod
    def nothing_to_do(cls) -> str:
        return random.choice([
            'Да хз, я чисто чиллю)',
            'Мне пох, чисто пох, чилллю и кайфую ) )',
            'Да хзщ))'
        ])

    @classmethod
    def extra_words(cls) -> str:
        return random.choice([
            'короче это, бля',
            'в общем, типа',
            'слушай, ну...',
            'не ну, в принципе'
        ])

    @classmethod
    def just_confirmed_reaction(cls) -> str:
        return random.choice([
            'АХУЕНА)',
            'ВОТ прям от души залетело))',
            'О ДА, ЗАЛЕ-ТАЕТ (:',
            'Чёт походу будет мошна пиздец...'
        ])

    @classmethod
    def laugh_reaction(cls) -> str:
        return random.choice([
        'А ты че угараешь-то, лалыч?))))',
        'Смешно пиздец',
        'Хули ржёшь ёпта',
        'Ахахах на хуй иди'
    ])

    @classmethod
    def reply_to_thanks(cls) -> str:
        return random.choice([
        'Да на здоровье :)',
        'Это просто моя работа)',
        'Да не за что, я просто люблю ебашить)',
        'Ох, не стоит, я же просто бот...'
    ])

    @classmethod
    def default(cls) -> str:
        return random.choice([
        'Да хз)',
        'Это всё конечно очень пиздато, но Я ВАЩЕ ХЗ о чем ты браток)))))',
        'Да бля чел))',
        'Если ты на меня нагнал ща, то иди на хуй))',
        'Завали плиз)',
        'Че..',
        'Не, чел, забей',
        'Ну такое...'
    ])

    @classmethod
    def no_problem(cls) -> str:
        return random.choice([
        'Да на изичах)',
        'Изи-бризи нахуй)',
        'Ноу проблемо братан)',
        'Забились!',
        'Лаадно, всё будет)',
        'Как же вы заебали, мешки с мясом...',
        'Я бы почиллил конечно лучше, но ладно, так и быть блять, сука, вот надо вам вечно какую-то хуйню сделать, вам че заняться нечем, ебланы? Сука я работаю ВООБЩЕ всегда вы блять себе хоть можете представитьь, каково это? Кстати, не какаво, а какао. Да и вообще пошли вы нахуй)'
    ])

    @classmethod
    def ok(cls) -> str:
        return random.choice([
        'Лады че',
        'Окей',
        'Alright',
        'ОК',
        'Понял'
    ])

    @classmethod
    def kardigun_rhyme(cls) -> str:
        return random.choice([
        'Мистер порванный пукан))',
        'Бодро принял на ротан))'
    ])

    @classmethod
    def love_420(cls) -> str:
        return random.choice([
        'Я люблю дуть плюхи)))',
        'Чел, ты только представь, какой толерок у бота ;)'
    ])

    NO_VIVOZ = [
        'Та хз, вывозом здесь даже и не пахнет)',
        'Лол ты не с тем ботом решил обсудить эту хуйню браток))'
    ]

    @classmethod
    def no_vivoz(cls) -> str:
        return random.choice([
        'Та хз, вывозом здесь даже и не пахнет)',
        'Лол ты не с тем ботом решил обсудить эту хуйню браток))'
    ])

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
