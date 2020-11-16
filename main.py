# %%

import collections
import requests


class OxfordAPI:

    def __init__(self, app_id, app_key, language='en-gb', fields='definitions,examples', strict=False):
        # init api with parameters

        self.app_id = app_id
        self.app_key = app_key
        self.language = language
        self.fields = fields
        self.strict = strict

        self.entries_root = 'https://od-api.oxforddictionaries.com/api/v2/entries/{}/REPLACE_TEXT?fields={}&strictMatch={}'.format(
            self.language, self.fields, self.strict)
        self.lemmas_root = 'https://od-api.oxforddictionaries.com/api/v2/lemmas/{}/REPLACE_TEXT'.format(
            self.language)

    def get(self, word):
        # send request to api for word

        entry_url = self.entries_root.replace('REPLACE_TEXT', word)
        lemma_url = self.lemmas_root.replace('REPLACE_TEXT', word)

        try:
            # request the OXFORD API for the definition
            response = requests.get(
                entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # if request failed, rerun with lemma
            response = requests.get(
                lemma_url, headers={"app_id": self.app_id, "app_key": self.app_key})

        return Word(response.json())


class Word:

    def __init__(self, raw_text):
        self.raw_text = raw_text

    @property
    def entries(self):
        return self.raw_text['results'][0]['lexicalEntries']

    @property
    def flattened_entries(self):
        return [flatten(entry) for entry in self.entries]


def flatten(data):

    obj = collections.OrderedDict()

    def recurse(data, key=""):
        if isinstance(data, list):
            for i in range(len(data)):
                recurse(data[i], '{}.{}'.format(key, i) if key else str(i))
        elif isinstance(data, dict):
            for k, v in data.items():
                recurse(v, '{}.{}'.format(key, k) if key else k)
        else:
            obj[key] = data

    recurse(data)

    return obj


id = "73629f11"
key = "e3713b7c303a270fb1827a72a4c233b3"
dictionary = OxfordAPI(id, key)

word = dictionary.get('obverse')
