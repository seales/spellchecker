
import re
import traceback
import os
import enchant
import keyword

import config.config as config

from spelling.spelling_error_group import SpellingErrorGroup
from glob import glob


STRIP_REGEX = re.compile('[^a-zA-Z]')

d = enchant.Dict("en_US")


def recursively_get_all_files_in_path(path):
    python_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.py'))]
    md_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.md'))]
    markdown_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.markdown'))]
    rst_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.rst'))]
    return python_files + rst_files + md_files + markdown_files


def get_all_files_in_directory(path):
    return glob(path + "/*" if path[-1] != "/" else path + "*.txt")


def print_error():

    """
    Method to-be-invoked when exception occurs.
    """

    traceback.print_exc()
    print("\n\nSomething unexpected just happened. Please create an issue - https://github.com/seales/spellchecker")


def strip_string(string):

    """
    Removes all non-alphas from input.

    :param string: str
    :return: str
    """

    return STRIP_REGEX.sub(" ", string)


def consolidate_spelling_errors(spelling_errors):

    """
    Groups input SpellingError list into SpellingErrorGroups, using the misspelled word as a hash key.

    :param spelling_errors: [SpellingError]
    :return: [SpellingErrorGroup]
    """

    spelling_error_hash = {}

    print("\nFound " + str(config.spelling_error_counter) + " suspicious words. Trying to filter...")

    for error in spelling_errors:

        lower_error_word = error.word.lower()  # make key case-insensitive

        if lower_error_word not in spelling_error_hash:
            spelling_error_hash[lower_error_word] = {"count": 1, "error_list": [error]}
        else:
            spelling_error_hash[lower_error_word]["count"] += 1
            spelling_error_hash[lower_error_word]["error_list"] += [error]

    print("\nDone filtering...")
    total_remaining_count = 0
    for key in sorted(spelling_error_hash.keys()):
        if spelling_error_hash[key]["count"] < 5:
            total_remaining_count += 1
        else:
            del spelling_error_hash[key]


    if total_remaining_count == 0:
        print("\nNo suspicious words remain.")
    else:
        print("\nOnly " + str(total_remaining_count) + " suspicious words remain. Help me investigate.")

    return spelling_group_list_from_hash(spelling_error_hash)


def spelling_group_list_from_hash(spelling_error_hash):

    """
    Converts SpellingErrors, within a dictionary that has each misspelled word
    as a key, into SpellingErrorGroups.

    :param spelling_error_hash: dict
    :return: [SpellingErrorGroup]
    """

    spelling_error_list = []

    for key in spelling_error_hash.keys():
        group = SpellingErrorGroup(key, spelling_error_hash[key]["error_list"])
        spelling_error_list.append(group)

    return spelling_error_list


def print_spelling_error_group_list(spelling_error_group_list, investigated_indices):

    """
    Print the suspicious word associated with each SpellingErrorGroup in the input. If a word
    has been investigated, we mark it.

    :param spelling_error_group_list: [SpellingErrorGroup]
    """

    print("")
    index = 0
    for group in spelling_error_group_list:
        output_str = str(index) + " -- " + group.word

        if index in investigated_indices:
            output_str += " <-- [investigated]"

        print(output_str)
        index += 1


def print_spelling_error_group(spelling_error_group):

    """
    Print the file line associated with each SpellingError in the input SpellingErrorGroup.

    :param spelling_error_group: SpellingErrorGroup
    """

    print("")
    index = 0
    for spelling_error in spelling_error_group.group:
        print(str(index) + " -- " + repr(spelling_error.line.strip(" ")))
        index += 1


def print_bound_message(bound):

    """
    Used when user inputs invalid integer selection.

    :param bound: str
    """

    print("\nYour input must be an integer between 0 and " + bound + ". Try again.")


def split_line(line):

    # TODO - split each line in the file more intelligently

    """
    Attempt to split input into individual words.

    :param line: str
    :return: str
    """

    return strip_string(convert_camel_case_to_underscore(line))\
        .replace("-", " ").replace("_", " ").replace("=", " ").split(" ")


def convert_camel_case_to_underscore(name):

    """
    Convert camel case to underscore.

    :param name: str
    :return: str
    """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)


def update_file(error, correct_word):

    """
    Uses input SpellingError to update occurrence in file with correct_word param.

    :param error: SpellingError
    :param correct_word: str
    """

    try:
        with open(error.file, 'r') as file:
            data = file.readlines()

        line_index = int(error.line_number) - 1
        start_index = data[line_index].lower().index(error.word.lower())
        end_index = start_index + len(error.word)

        data[line_index] = data[line_index][0:start_index] + correct_word + data[line_index][end_index:]

        with open(error.file, 'w') as file:
            file.writelines(data)

    except Exception:
        print_error()


def remove_non_utf8(line):

    """
    Strips all non-utf8 from input.

    :param line: str
    :return: str
    """

    # TODO - handle for both python2/3

    try:
        return line  # line.encode('utf-8').decode('utf-8', 'ignore').encode("utf-8")
    except Exception:
        return ""


def is_two_part_word(word):

    """
    Returns true if input is composed of two words.

    :param word: str
    :return: bool
    """

    # TODO - make more complex (N-part word, rather than 2-part word)

    for i in range(1, len(word)-1):

        left = word[0:i]
        right = word[i:]
        if d.check(left) and d.check(right):
            # FIXME - hack implemented because Enchant views "l" as a valid word
            if (len(left) == 1 and left != 'a') or (len(right) == 1 and right != 'a'):
                continue
            return True
    return False


def is_spelling_error(word):

    """
    Returns true if the word seems to be misspelled; this is determined
    by the user-specified languages.

    :param word: str
    :return: bool
    """

    # TODO - use users language selection when assessing spelling correctness

    return word and not d.check(word.upper()) and not keyword.iskeyword(word) and not is_two_part_word(word)

