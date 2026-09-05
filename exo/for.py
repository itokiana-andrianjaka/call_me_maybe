# def take_last_words_params(string: str, char: str) -> str:
#     i: int = len(string) - 1
#     while i >= 0 and string[i] != char:
#         i -= 1
#     i -= 1
#     count: int = 0
#     while i >= 0 and string[i] != char:
#         count += 1
#         i -= 1
#     start_index: int = i + 1
#     return string[start_index:start_index + count]

# def take_last_words_params(string: str, char: str) -> str | None:
#     parts = string.split(char)
#     if len(parts) < 3 or len(parts) % 2 == 0:
#         return None
#     return parts[-2]

# if __name__ == "__main__":
#     ex1 = 'This is a "sample string" "with" "some words".'
#     print(take_last_words_params(ex1, '"'))  # some words

#     ex2 = '"with" "some words".""'
#     print(take_last_words_params(ex2, '"'))  # None

# try:
#     raise ValueError(
#         "A simple security check failed (due to a missing '\"')\n\
# [Should never be raised]")
# except ValueError as e:
#     print(e)
# for i in range(5):
print("}")
