import logging
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class MapClient:
    STATIC_API_URL: ClassVar[str] = 'https://static-maps.yandex.ru/1.x/'

    IMAGE_SIZE = 300
    LANG_SYMBOL = 'ru_RU'
    MAP_TYPE = 'map'
    ZOOM = 14

    def get_img_link_by_coordinates(self, coordinates: [float, float]) -> str:
        params = {
            'size': f'{self.IMAGE_SIZE},{self.IMAGE_SIZE}',
            'lang': self.LANG_SYMBOL,
            'l': self.MAP_TYPE,
            'z': self.ZOOM,
            'll': f'{coordinates[1]},{coordinates[0]}',
            'pt': f'{coordinates[1]},{coordinates[0]},flag',
        }
        params_str = '&'.join(f'{k}={v}' for k, v in params.items())

        res = f'{self.STATIC_API_URL}?{params_str}'
        logging.debug(f'\n-----> {res}')

        return res
