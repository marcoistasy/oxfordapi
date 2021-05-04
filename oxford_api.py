from results import Word
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

        try:

            # try to get data from API using input word

            # rereference entry root to include word
            entry_url = self.entries_root.replace('WORD_SEARCH', word.lower())

            # request the API for the definition
            response = requests.get(
                entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})
            response.raise_for_status()

        except requests.exceptions.HTTPError:

            # if request failed, rerun with lemma

            # rereference lema root to include word
            lemma_url = self.lemmas_root.replace('WORD_SEARCH', word.lower())

            # request API for headword
            response = requests.get(
                lemma_url, headers={"app_id": self.app_id, "app_key": self.app_key})

            # rerun with inflection
            self.get(OxfordAPI._remove_lemma(response))

        return Word(response.json())

    @staticmethod
    def _remove_lemma(response):
        return response.json()['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']
