global file_counter
global total_file_count
global spelling_error_counter

file_counter = 0
total_file_count = 0
spelling_error_counter = 0

UPPER_BOUND_PER_THREAD = 400  # chosen somewhat arbitrarily
REVIEW_GROUP_SIZE = 15  # chosen to be the most errors that can easily be viewed at once
STATUS_PRINT_INTERVAL = 10  # print status when the number of files read is divisible by this number

