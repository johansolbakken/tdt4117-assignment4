#!/usr/bin/env python3

import math

s = "Intelligent behavior in people is a product of the mind. But the mind itself is more like what the human brain does.".split()
n = 4
length = int(math.ceil(len(s) / n))
blocks = [s[i:i+length] for i in range(0, len(s), length)]
print(blocks)