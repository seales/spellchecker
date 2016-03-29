
"""
Command-line spellchecker.

NOTE: Program assumes that entirety of search can fit into memory; this assumption may not cover your use-case.
"""

import time
import copy
import os.path

import config.config as config
import common.utils as utils

from spelling.spelling_worker import SpellingWorker


# TODO - make python 2/3 friendly


def discover_spelling_errors(files):

    """
    Creates SpellingWorker(s) to assess the spelling of the all files in the user-specified path.

    :param files: [str]
    :return: [SpellingErrorGroup]
    """

    config.file_counter = 1
    config.spelling_error_counter = 0
    config.total_file_count = len(files)

    start_time_epoch_seconds = time.time()
    workers = []
    spelling_errors = []

    for i in range(0, len(files), config.UPPER_BOUND_PER_THREAD):

        # give each thread a set number of files
        worker = SpellingWorker(files[i:i+config.UPPER_BOUND_PER_THREAD], start_time_epoch_seconds)

        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()
        spelling_errors += copy.deepcopy(worker.spelling_errors)

    for worker in workers:
        del worker

    return utils.consolidate_spelling_errors(spelling_errors)


def review_spelling_error(spelling_error):

    """
    Allows the user to review a single SpellingError. The, potentially-updated,
    SpellingError is returned so that the caller can be aware of the change.

    :param spelling_error: SpellingError
    :return SpellingError
    """

    while True:
        print("\nThe suspect word, " + repr(spelling_error.word)
              + ", appears in \n\t" + repr(spelling_error.line.strip(" ")))

        correction = ask_for_input("\nTell me how to fix, or enter 'n' to continue. >> ")

        if correction.upper() == "N":
            return spelling_error
        else:

            verification = ask_for_input("\nYou want to replace " + repr(spelling_error.word)
                                     + " with " + repr(correction) + ". Enter 'y' or 'n'. >> ")

            if verification.upper() == "Y":
                utils.update_file(spelling_error, correction)

                # update so as to not confuse user
                spelling_error.line = spelling_error.line.replace(spelling_error.word, correction)
                spelling_error.word = correction

                return spelling_error
            elif verification.upper() == "N":
                print("\nOkay, I'll ask you again.\n")
            else:
                print("\nI didn't understand your input. Please try again.\n---\n")


def review_spelling_error_group(spelling_error_group):

    """
    Allows the user to review a single SpellingErrorGroup. The, potentially-updated,
    SpellingErrorGroup is returned so that the caller can be aware of the change.

    :param spelling_error_group: [SpellingErrorGroup]
    :return SpellingErrorGroup
    """

    if len(spelling_error_group.group) == 1:
        spelling_error_group.group = [review_spelling_error(spelling_error_group.group[0])]
        return spelling_error_group

    print("\n---\n\nYou chose to investigate " + repr(spelling_error_group.word) + ". Here are appearances of it...")

    while True:

        utils.print_spelling_error_group(spelling_error_group)

        user_selection = ask_for_input("\nEnter number to correct, otherwise enter 'n'. >> ")

        if user_selection.upper() == "N":
            return spelling_error_group  # user has completed review
        else:

            is_original_pass = True

            while True:

                if not is_original_pass:
                    print("\n---")
                    utils.print_spelling_error_group(spelling_error_group)
                    user_selection = ask_for_input("\nEnter number to correct, otherwise enter 'n'. >> ")
                else:
                    is_original_pass = False

                if user_selection.upper() == "N":
                    return spelling_error_group
                else:
                    if user_selection.isdigit():
                        selected_index = int(user_selection)

                        if 0 <= selected_index <= len(spelling_error_group.group):

                            # update so as to not confuse user
                            spelling_error_group.group[selected_index] = \
                                review_spelling_error(spelling_error_group.group[selected_index])
                        else:
                            utils.print_bound_message(str(len(spelling_error_group.group)-1))

                    else:
                        utils.print_bound_message(str(len(spelling_error_group.group)-1))


def review_spelling_error_group_list(words_seen, total_words, spelling_error_group_list):

    """
    Allows the user to review a SpellingErrorGroup list. The purpose is to segment
    all SpellingErrorGroup(s) and review each segment through calls to this method.

    Returns boolean regarding whether the program should backup.

    :param words_seen: int
    :param total_words: int
    :param spelling_error_group_list: [SpellingErrorGroup]
    :return bool
    """

    investigated_indices = []

    while True:

        print("\n---")
        utils.print_spelling_error_group_list(spelling_error_group_list, investigated_indices)

        user_selection = ask_for_input("\nSeen " + str(words_seen)
                                   + " words out of " + str(total_words)
                                   + ". Enter number to investigate, 'b' to backup, or 'n' to skip. >> ")

        if user_selection.upper() == "N":
            return False  # user has completed review
        elif user_selection.upper() == "B":
            return True
        else:
            if user_selection.isdigit():

                selected_index = int(user_selection)

                if 0 <= selected_index <= len(spelling_error_group_list):

                    # update so as to not confuse user
                    spelling_error_group_list[selected_index] = \
                        review_spelling_error_group(spelling_error_group_list[selected_index])

                    investigated_indices.append(selected_index)
                else:
                    utils.print_bound_message(str(len(spelling_error_group_list)-1))
            else:
                utils.print_bound_message(str(len(spelling_error_group_list)-1))


def review_spelling_errors(spelling_error_group_list):

    """
    Allows the user to review a SpellingErrorGroup list. Effectively, all
    spelling errors found in user-specified path.

    :param spelling_error_group_list: [SpellingErrorGroup]
    """

    spelling_error_index = 0
    segmented_spelling_error_group = []

    while spelling_error_index < len(spelling_error_group_list):
        segmented_spelling_error_group.append(spelling_error_group_list[spelling_error_index])
        spelling_error_index += 1

        if len(segmented_spelling_error_group) >= config.REVIEW_GROUP_SIZE:
            backup = review_spelling_error_group_list(spelling_error_index,
                                                      len(spelling_error_group_list), segmented_spelling_error_group)

            if backup:
                spelling_error_index -= (2*config.REVIEW_GROUP_SIZE)
                if spelling_error_index < 0:
                    spelling_error_index = 0  # we should never have a negative indices

            segmented_spelling_error_group = []
        elif (len(spelling_error_group_list) - spelling_error_index) + len(segmented_spelling_error_group)\
                < config.REVIEW_GROUP_SIZE:
            backup = review_spelling_error_group_list(len(spelling_error_group_list),
                                                      len(spelling_error_group_list),
                                                      spelling_error_group_list[spelling_error_index-1:])
            spelling_error_index = len(spelling_error_group_list)

            if backup:
                spelling_error_index -= (2*config.REVIEW_GROUP_SIZE)
                if spelling_error_index < 0:
                    spelling_error_index = 0  # we should never have a negative indices
            else:
                break
            segmented_spelling_error_group = []



def ask_for_input(output_to_user):

    """
    Handles Python2/3 discrepancy.

    :param output_to_user: str
    """

    try:
        return raw_input(output_to_user)
    except NameError:
        return input(output_to_user)

def main():

    """
    Loops while user specifies a directory to search.
    """

    try:
        while True:
            directory_input = ask_for_input("\nEnter directory or 'q' to quit. >> ")

            if directory_input.upper() == "Q":
                print("\nExiting now...\n")
                break
            elif os.path.isdir(directory_input):
                print("\nYou entered: " + repr(directory_input) + "\n")
                files = utils.recursively_get_all_files_in_path(directory_input)
                spelling_error_group_list = discover_spelling_errors(files)
                review_spelling_errors(spelling_error_group_list)
            else:
                print("\nI couldn't find the directory: " + repr(directory_input) + ". Try again.")

    except Exception:
        utils.print_error()
        print("\nExiting now...\n")


if __name__ == '__main__':
    main()
