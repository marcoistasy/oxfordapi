from word import Word
import requests


class OxfordAPI:

    def __init__(self, app_id, app_key, language='en-gb', filters=None, strict=False):

        # init api with parameters
        self.app_id = app_id
        self.app_key = app_key
        self.language = language
        self.filters = filters
        self.strict = strict

        # define filters if None
        if self.filters is None:
            self.filters = 'definitions,domains,etymologies,examples,pronunciations,regions,registers,variantForms'

        # reference http point for API

        self._base_root = 'https://od-api.oxforddictionaries.com/api/v2/ENTRY_POINT/{}/WORD_SEARCH?fields={}&strictMatch={}'.format(
            self.language, self.filters, self.strict)

        self.entries_root = self._base_root.replace('ENTRY_POINT', 'entries')
        self.lemmas_root = self._base_root.replace('ENTRY_POINT', 'lemmas')

    def get(self, word):

        # make sure input is a headword by referencing lemma
        lemma_url = self.lemmas_root.replace('WORD_SEARCH', word.lower())
        lemma_response = requests.get(
            lemma_url, headers={"app_id": self.app_id, "app_key": self.app_key})
        head_word = lemma_response.json(
        )['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']

        # ask API
        entry_url = self.entries_root.replace('WORD_SEARCH', head_word.lower())
        response = requests.get(
            entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})

        return Word(response.json())
