# %%

import requests
from oxford_api import OxfordAPI

# oxford_id = "73629f11"
# oxford_key = "e3713b7c303a270fb1827a72a4c233b3"
# dictionary = OxfordAPI(oxford_id, oxford_key)

# word = dictionary.get('translations')

#%%
# print(word.entries[0].senses[0].definition)

remnote_key = '59317628adc125d07aed2e82271ee400'
remnote_id = 'bmMEYKHZ3rMs3fH34'
page_id = 'nbMLTanczSK6zx6iv'
remnote_create = 'https://api.remnote.io/api/v0/create'



#%%

input = {'apiKey': remnote_key, 'userId': remnote_id, 'parentId': page_id,
  'text': 'My new Rem #[[Extra Card Detail]]',
  'positionAmongstSiblings': 0,
}
x = requests.post(remnote_create, input)
print(x.text)



# %%
