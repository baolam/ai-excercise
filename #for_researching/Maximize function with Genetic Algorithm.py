import random
import math
from typing import Final
from typing import List

POP_SIZE : Final = 20 # Kích thước quần thể
THETA : Final = 0.5 # Xác suất sinh một bit (r >= theta -> bit 1 otherwise bit 0)
PRECISION : Final = 6
CROSS_OVER_PROBABILITY = 0.25
REMOVE_INDIVIDUAL_CROSSOVER = 0.2
MUTATION_PROBABILITY = 0.01

f = open("config.txt", "r", encoding="utf-8")
M = 0
ranges = []
m_bits = []

k = int(f.readline())
for __ in range(k):
  a, b = list((map(lambda x : float(x), f.readline().split(' '))))
  ranges.append((a, b))
  bits = math.ceil(math.log2((b - a) * (10 ** 4) + 1))
  m_bits.append(bits)
  M += bits

print("Tổng số bit cần dùng để mã hóa là:", M)

def generate_individual():
  individual = ""
  for i in range(M):
    r = random.random()
    if r < THETA:
      individual += "0"
    else:
      individual += "1"
  return individual

# Khởi tạo quần thể
population = []
for __ in range(POP_SIZE):
  population.append(generate_individual())

# Đánh giá độ thích nghi của cá thể
def eval(individual : str):
  def f(X : List[float]):
    val = 21.5 + X[0] * math.sin(4 * math.pi * X[0]) + X[1] * math.sin(20 * math.pi * X[1])
    return round(val, PRECISION)

  def __get_value(bits : str):
    rbits = bits[::-1]
    val = 0
    for i in range(len(rbits)):
      val += int(rbits[i]) * (2 ** i)
    return val

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
  
  return f(decode(individual))

# print(decode("000010000011001000001010111011101"))
# print(eval("000010000011001000001010111011101"))

# Lựa chọn các cá thể mới
def selection():
  evals = [ eval(individual) for individual in population ]
  p = [0] * POP_SIZE 
  q = [0] * POP_SIZE
  F = sum(evals)

  # Tính xác suất
  for i in range(POP_SIZE):
    p[i] = round(evals[i] / F, PRECISION)
    if i == 0: q[i] = p[i]
    else:
      q[i] = round(q[i - 1] + p[i], PRECISION)
  
  return F, p, q

# Bánh xe rudet
def routtle():
  pass

# Lai ghép cá thể
def crossover():
  def get_parents():
    _pairs = []

    # Tiến hành lựa chọn các cá thể tham gia vào lai ghép
    for i in range(POP_SIZE):
      r = random.random()
      if r < CROSS_OVER_PROBABILITY:
        _pairs.append(i)  

    # Xử lí khi số cá thể được chọn là số lẻ
    if len(_pairs) % 2 != 0:
      r = random.random()
      if r > REMOVE_INDIVIDUAL_CROSSOVER:
        _pairs.pop()
      else:
        _pairs.append(random.randint(0, POP_SIZE - 1))
    
    # Nhóm cặp
    pairs = []
    for i in range(0, len(_pairs), 2):
      pairs.append((_pairs[i], _pairs[i + 1]))

    return pairs
      
  return get_parents()

# print(crossover())