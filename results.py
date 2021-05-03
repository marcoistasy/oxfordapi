class Entry:
    
    def __init__(self, definition = None, category = None, domain = None, subsense = None, example = None):

        self.definition = definition
        self.category = category
        self.domain = domain
        self.subsense = subsense
        self.example = example


class Word:

    def __init__(self, raw_text):

        self.raw_text = raw_text
        self.results = self.raw_text['results'][0]['lexicalEntries']
        self.entries = []

        try:
            self._parse()
        except:
            print('unable to parse word')

    def _parse(self):

        # iterate over results
        for result in self.results:
            
            # get lexical category for each result
            lexical_category = result['lexicalCategory']['text']
            
            # iterate over entry in results
            for entry in result['entries']:

                # declare Entry instance
                result = Entry()
                result.category = lexical_category

                # iterate over sense in entry
                for sense in entry['senses']:

                    # get definition for sense
                    result.definition = sense['definitions']

                    # iterate over subsenses
                    if 'subsenses' in sense:

                        for subsense in sense['subsenses']:

                            result.subsense = subsense['definitions']

                    # iterate over domains
                    if 'domains' in sense:

                        for domain in sense['domains']:

                            result.domain = domain['text']
                    
                    # iterate over examples
                    if 'examples' in sense:

                        for example in sense['examples']:

                            result.example = example['text']

                    self.entries.append(result)
