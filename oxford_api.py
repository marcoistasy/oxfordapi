from results import Word
import requests

class OxfordAPI:

    def __init__(self, app_id, app_key, language='en-gb', fields='definitions,domains,examples', strict=False):
        # init api with parameters

        self.app_id = app_id
        self.app_key = app_key
        self.language = language
        self.fields = fields
        self.strict = strict

        self.entries_root = 'https://od-api.oxforddictionaries.com/api/v2/entries/{}/REPLACE_TEXT?fields={}&strictMatch={}'.format(self.language, self.fields, self.strict)
        self.lemmas_root = 'https://od-api.oxforddictionaries.com/api/v2/lemmas/{}/REPLACE_TEXT'.format(self.language)

    def get(self, word):

        # send request to api for word
        entry_url = self.entries_root.replace('REPLACE_TEXT', word.lower())
        lemma_url = self.lemmas_root.replace('REPLACE_TEXT', word.lower())

        try:
            
            # request the OXFORD API for the definition
            response = requests.get(entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            
            # if request failed, rerun with lemma
            response = requests.get(lemma_url, headers={"app_id": self.app_id, "app_key": self.app_key})

            entry_url = self.entries_root.replace('REPLACE_TEXT', OxfordAPI._remove_lemma(response))
            response = requests.get(entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})

        return Word(response.json())

    @staticmethod
    def _remove_lemma(response):
        return response.json()['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']
