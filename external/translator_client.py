import logging
from dataclasses import dataclass
from typing import List, Optional

import requests

from env import settings


@dataclass
class TranslatorClient:
    host: str = 'google-translate1.p.rapidapi.com'
    base_url: str = f'https://{host}'

    def get_languages(self) -> List[str]:
        url = f'{self.base_url}/language/translate/v2/languages'

        headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': settings.translator_api_key,
            'accept-encoding': 'application/gzip'
        }

        response = requests.get(url, headers=headers)

        return response.text.split()

    def translate(self, text: str) -> Optional[str]:
        url = f'{self.base_url}/language/translate/v2'

        payload = f'source=ru&q={text}&target=en'
        headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': settings.translator_api_key,
            'accept-encoding': 'application/gzip',
            'content-type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            return None

        translation_info = response.json().get('data')
        if not translation_info:
            return 'Хз чёт...'

        translations = translation_info.get('translations')
        if not translations:
            return 'Хз чёт...'

        return translations[0].get('translatedText', 'Хз чёт...')
