#!/usr/bin/env python3

s = "Intelligent behavior in people is a product of the mind. But the mind itself is more like what the human brain does."
s = s.lower()
# (text, column)
tokens = []

# Split the string into words and enumerate them to capture the index
for index, word in enumerate(s.split()):
    # Find the start position of the word in the string
    start_pos = s.find(word)
    # Append the word and its start position to the tokens list
    tokens.append((word, start_pos + 1))

# Output the list of tokens and their columns
for token in tokens:
    print(token[0], token[1], sep="\t")