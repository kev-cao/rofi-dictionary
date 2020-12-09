import requests
import json

class ApiRequester:
    """
    Object that will retrieve data from the Oxford Dictionary API.
    """
    def __init__(self):
        with open('app_values.json', 'r') as f:
            app_values = json.load(f)

        self.app_key = app_values['app_key']
        self.app_id = app_values['app_id']
        self.lang = "en-gb"
        self.results = []

    def query(self, word):
        """
        Queries the Oxford Dictionary API for the definitions of the given word
        and sets results attribute to the sense sequences of the word.

        Parameters:
        word (String): The query word.
        """
        dictionary_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{self.lang}/{word}"
        response = requests.get(dictionary_url, headers={'app_id': self.app_id, 'app_key': self.app_key}).json()
        self.results = response['results']

    def get_results_preview(self):
        """
        Gets a preview of all results in a list.

        Return:
        list: A list of preview objects that show the lexical category.
        """
        return [result['lexicalEntries'][0]['lexicalCategory'] for result in self.results]

    def get_senses_definitions(self, idx=0, ndefs=3):
        """
        Gets the definitions from a set of senses from the results.

        Parameters:
        idx (Integer): The index of the senses set in the results.
        ndefs (Integer): The number of definitions desired.

        Returns:
        list: A list of definitions.
        """
        senses = self.results[idx]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = []

        for i in range(min(ndefs, len(senses))):
            definitions.append(senses[i]['definitions'][0])

        return definitions
