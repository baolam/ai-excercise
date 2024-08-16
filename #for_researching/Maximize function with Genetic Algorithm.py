import random
import math
from typing import Final
from typing import List

POP_SIZE : Final = 50 # Kích thước quần thể
THETA : Final = 0.5 # Xác suất sinh một bit (r >= theta -> bit 1 otherwise bit 0)
PRECISION : Final = 6

f = open("config.txt", "r", encoding="utf-8")
N_BITS = 0
ranges = []
m_bits = []
k = int(f.readline())
for __ in range(k):
  a, b = list((map(lambda x : float(x), f.readline().split(' '))))
  ranges.append((a, b))
  bits = math.ceil(math.log2((b - a) * (10 ** 4) + 1))
  m_bits.append(bits)
  N_BITS += bits

print("Tổng số bit cần dùng để mã hóa là:", N_BITS)

def generate_individual():
  individual = ""
  for i in range(N_BITS):
    r = random.random()
    if r < THETA:
      individual += "0"
    else:
      individual += "1"
  return individual

population = []
for __ in range(POP_SIZE):
  population.append(generate_individual())

def __get_value(bits : str):
  rbits = bits[::-1]
  val = 0
  for i in range(len(rbits)):
    val += int(rbits[i]) * (2 ** i)
  return val

def f(X : List[float]):
  val = 21.5 + X[0] * math.sin(4 * math.pi * X[0]) + X[1] * math.sin(20 * math.pi * X[1])
  return round(val, PRECISION)

def decode(individual : str):
  x = []
  tmp = 0
  sum = 0
  for i in range(len(m_bits)):
    sum += m_bits[i]
    _x = individual[tmp:sum]
    a, b = ranges[i]
    _x = a + __get_value(_x) * (b - a) / (2 ** m_bits[i] - 1)
    x.append(round(_x, PRECISION))
    tmp += m_bits[i]
  return x

def eval(individual : str):
  return f(decode(individual))

# print(decode("000010000011001000001010111011101"))
# print(eval("000010000011001000001010111011101"))