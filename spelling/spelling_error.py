
class SpellingError:

    def __init__(self, file, word, line, line_number):

        """
        Takes file_path, misspelled word, line where misspelling occurs, and line number of misspelling.

        :param file: str
        :param word: str
        :param line: str
        :param line_number: int
        """

        self.__file = file
        self.__word = word
        self.__line = line
        self.__line_number = line_number

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, file):
        self.__file = file

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, word):
        self.__word = word

    @property
    def line(self):
        return self.__line

    @line.setter
    def line(self, line):
        self.__line = line

    @property
    def line_number(self):
        return self.__line_number

    @line_number.setter
    def line_number(self, line_number):
        self.__line_number = line_number

