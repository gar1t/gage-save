import json
import math
import random

__gage__ = """
flags:
  x:
    bind: config.json:x
  noise:
    bind: config.json:noise
"""

__gage_v2__ = """
flags.bind: config.json
"""

__gage_v3__ = """
flags.bind:
  - config1.json
  - config2.json
"""

config = json.load(open("config.json"))

x = config["x"]
noise = config["y"]

print("x: %f" % x)
print("noise: %f" % noise)

loss = math.sin(5 * x) * (1 - math.tanh(x**2)) + random.random() * noise

print("loss: %f" % loss)
