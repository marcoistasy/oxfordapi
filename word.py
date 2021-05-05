class Word:
    # class to hold word returned from the Oxford API

    def __init__(self, raw_text):
        # init parameters of entry -- needs only a raw JSON object
        self.raw_text = raw_text
        self.entries = []

        try:
            self._parse()
        except KeyError:
            print('Unable to parse word. Please debug.')

    def _parse(self):

        # iterate over results
        for result in self.raw_text['results']:

            # iterate over entry
            for e in result['lexicalEntries']:

                # create and entry
                entry = Entry(str(e['lexicalCategory']['id']))

                # # iterate over sense in entry
                for s in e['entries'][0]['senses']:

                    # create sense object with supplementary information
                    sense = Sense(str(s['definitions'][0]), s)
                    entry.senses.append(sense)

                self.entries.append(entry)


class Entry:
    # class to hold a sense for a given word organised under grammatical category

    def __init__(self, grammatical_category):
        # init parameters of entry -- needs only a grammatical_category

        self.grammatical_category = grammatical_category
        self.senses = []


class Sense:
    # class to hold a given sense in an entry

    def __init__(self, definition, raw_information):
        # init parameters of sense -- needs only a defintion and raw JSON object

        self.definition = definition
        self.examples = []
        self.domains = []
        self.registers = []
        self.subsenses = []

        self._add_supplementary_information(raw_information)

    def _add_supplementary_information(self, raw_information):
        # adds information supplementary to a given sense --
        # may be extended to any of the various supplementary information provided by the Oxford API

        # domains
        if 'domains' in raw_information:
            self.domains = [i['text'] for i in raw_information['domains']]

        # examples
        if 'examples' in raw_information:
            self.examples = [i['text'] for i in raw_information['examples']]

        # registers
        if 'registers' in raw_information:
            self.registers = [i['text'] for i in raw_information['registers']]

        # subsenses
        if 'subsenses' in raw_information:
            self.subsenses = [Sense(i['definitions'][0], i)
                              for i in raw_information['subsenses']]
