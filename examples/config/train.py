import math
import random

# Hyperparameters
x = 0.1
noise = 0.1

print("x: %f" % x)
print("noise: %f" % noise)

# Simulated training loss
loss = math.sin(5 * x) * (1 - math.tanh(x**2)) + random.random() * noise

print("loss: %f" % loss)
