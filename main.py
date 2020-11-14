#%%
import requests
import time
import json

class OXFORD_API():

    def __init__(self, app_id, app_key, language='en-gb', fields='definitions,examples', strict=False):
        # init api with parameters

        self.app_id = app_id
        self.app_key = app_key
        self.language = language
        self.fields = fields
        self.strict = strict

        self.entries_root = 'https://od-api.oxforddictionaries.com/api/v2/entries/{}/REPLACE_TEXT?fields={}&strictMatch'.format(self.language, self.fields, self.strict)
        self.lemmas_root = 'https://od-api.oxforddictionaries.com/api/v2/lemmas/{}/REPLACE_TEXT'.format(self.language)

    def get(self, word):
        # send request to api for word

        entry_url = self.entries_root.replace('REPLACE_TEXT', word)
        lemma_url = self.lemmas_root.replace('REPLACE_TEXT', word)

        try:
            # request the OXFORD API for the definition
            response = requests.get(entry_url, headers={"app_id": self.app_id, "app_key": self.app_key})
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # if request failed, rerun with lemma
            response = requests.get(lemma_url, headers={"app_id": self.app_id, "app_key": self.app_key})

        return Word(response.json())


class Word():
    
    def __init__(self, raw_text):
        self.raw_text = raw_text

    @property
    def text(self):
        return self.raw_text['results']


app_id = "73629f11"
app_key = "e3713b7c303a270fb1827a72a4c233b3"
dictionary = OXFORD_API(app_id, app_key)

word = dictionary.get('hierophant')

#%%
data=word.text
print(data)

# %%
print(sasdfadf)
# print(json.dumps(x, indent=4))

# %%