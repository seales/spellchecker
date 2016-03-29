
class SpellingErrorGroup:

    def __init__(self, word, group):

        """
        Takes misspelled word and a list of relevant SpellingErrors.

        :param word: str
        :param group: [SpellingError]
        """

        self.__word = word
        self.__group = group

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, word):
        self.__word = word

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group):
        self.__group = group
