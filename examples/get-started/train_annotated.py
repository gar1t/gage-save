import math
import random

__vistaml__ = """
flags: [x]
requires: [data.txt]
scalars: [loss]
"""

__vistaml_v2__ = """
flags:
  x:
    bind: x
    type: default

requires:
  - type: file
    path: data.csv

scalars:
  loss:
    pattern: loss: (\val)
"""

x = 0.1
noise = 0.1

print("x: %f" % x)
print("noise: %f" % noise)

loss = math.sin(5 * x) * (1 - math.tanh(x**2)) + random.random() * noise

print("loss: %f" % loss)
