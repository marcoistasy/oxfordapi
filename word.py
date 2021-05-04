class Word:

    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.entries = []

        try:
            self._parse()
        except:
            print('unable to parse word')

    def _parse(self):

        # iterate over results
        for e in self.raw_text['results'][0]['lexicalEntries']:

            # create and entry
            entry = Entry(str(e['lexicalCategory']['id']))

            # # iterate over sense in entry
            for s in e['entries'][0]['senses']:

                # create sense object with supplementary information
                sense = Sense(str(s['definitions'][0]))
                sense.add_supplementary_information(s)

                # append to entry object
                entry.append_sense(sense)

            self.entries.append(entry)


class Entry:
    # class to hold an entry for a given word (organised under grammatical category)

    def __init__(self, lexical_category):
        self.lexical_category = lexical_category
        self.senses = []

    def append_sense(self, sense):
        self.senses.append(sense)


class Sense:
    # class to hold a given sense in an entry

    def __init__(self, definition, domains=None, subsense=None, example=None, registers=None):
        self.definition = definition
        self.domains = domains
        self.subsense = subsense
        self.example = example
        self.registers = registers

    def add_supplementary_information(self, supplementary_information):

        # domain
        if 'domains' in supplementary_information:
            self.domains = [i['text'] for i in supplementary_information['domains']]

        # example
        if 'examples' in supplementary_information:
            self.example = str(
                supplementary_information['examples'][0]['text'])

        # registers
        if 'registers' in supplementary_information:
            self.registers = [i['text'] for i in supplementary_information['registers']]

        # subsense
        if 'subsenses' in supplementary_information:
            self.subsense = str(
                supplementary_information['subsenses'][0]['definitions'][0])

