# %%

from oxford_api import OxfordAPI

id = "73629f11"
key = "e3713b7c303a270fb1827a72a4c233b3"
dictionary = OxfordAPI(id, key)

word = dictionary.get('idiopathic')

for i in word.entries:
    print(i.definition, i.domain, i.category, i.example, i.subsense)

# %%
