
import time
import os.path

import common.utils as utils
import config.config as config

from spelling.spelling_error import SpellingError
from threading import Thread


class SpellingWorker(Thread):

    def __init__(self, files, start_time):

        """
        Takes a list of file paths to check, and the start time of program initiation (in epoch seconds).

        :param files: [str]
        :param start_time: float
        """

        Thread.__init__(self)
        self.files = files
        self.start_time = start_time
        self.__spelling_errors = []

    @property
    def spelling_errors(self):
        return self.__spelling_errors

    def run(self):

        """
        Loops over all files and checks for spelling errors.
        """

        for file in self.files:

            config.file_counter += 1  # increment file-search count

            if file and os.path.isfile(file):
                self.read_file(open(file, "r"), file)

                if self.should_print_status(config.file_counter):
                    self.print_status()

    def read_file(self, readable_file, file_path):

        """
        Loops over each line in file.

        :param readable_file: file
        :param file_path: str
        """

        within_comment = False

        line_num = 1
        for line in readable_file:

            # TODO - only check comments and string literals

            # TODO - use file type to determine comment type, etc

            # TODO - for .txt; check everything (use utils.should_check_line method)

            # TODO - use each language's specific comment syntax

            # line = utils.remove_non_utf8(line)

            if line:

                if ".py" in file_path:
                    if within_comment:
                        if "\"\"\"" in line:
                            within_comment = False
                        self.read_line(line, file_path, line_num)
                    elif "#" in line:
                        self.read_line(line, file_path, line_num)
                    elif "\"\"\"" in line:
                        within_comment = True
                        self.read_line(line, file_path, line_num)
                else:
                    self.read_line(line, file_path, line_num)

            line_num += 1

    def read_line(self, line, file_path, line_num):

        """
        Assesses spelling of each word in line.

        :param line: str
        :param file_path: str
        :param line_num: int
        """

        # TODO - accept command line args regarding what to split on (e.g., comma, space, semi-colin, etc...)

        words = utils.split_line(line)

        for word in words:
            self.read_word(word, file_path, line, line_num)

    def read_word(self, word, file_path, line, line_num):

        """
        Assesses spelling of word.

        :param word: str
        :param file_path: str
        :param line: str
        :param line_num: int
        """

        # TODO - in future, loop over many possible dictionaries

        try:
            if utils.is_spelling_error(word):
                spelling_error = SpellingError(file_path, word, line, line_num)

                self.__spelling_errors.append(spelling_error)
                config.spelling_error_counter += 1  # new error, increment count
        except Exception:
            utils.print_error()

    @staticmethod
    def should_print_status(file_count):

        """
        Print search status if file_count is divisible by STATUS_PRINT_INTERVAL
        or the last file has been read.

        :param file_count: int
        :return: bool
        """

        return file_count % config.STATUS_PRINT_INTERVAL == 0 or file_count == config.total_file_count

    def print_status(self):

        elapsed_time = time.time() - self.start_time
        print(self.status(elapsed_time))

    @staticmethod
    def status(elapsed_time):

        """
        Constructs and returns a status update.

        :param elapsed_time: float
        :return: str
        """

        spelling_errs = "Suspicious Words: " + str(config.spelling_error_counter)
        file_progress = "Files Read: " + str(config.file_counter) + " out of " + str(config.total_file_count)
        time_progress = "In " + str("%.2f" % elapsed_time) + " seconds"

        return spelling_errs + " --- " + file_progress + " --- " + time_progress
