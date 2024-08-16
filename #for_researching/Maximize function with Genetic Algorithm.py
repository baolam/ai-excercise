import random
import math
from typing import Final
from typing import List

TOTAL_GENERATION = 1000
POP_SIZE : Final = 50 # Kích thước quần thể
THETA : Final = 0.5 # Xác suất sinh một bit (r >= theta -> bit 1 otherwise bit 0)
PRECISION : Final = 10
CROSS_OVER_PROBABILITY = 0.3
REMOVE_INDIVIDUAL_CROSSOVER = 0.5
MUTATION_PROBABILITY = 0.02

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
f.close()

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
def initalize() -> List[str]:
  population = []
  for __ in range(POP_SIZE):
    population.append(generate_individual())
  return population

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
# Bánh xe rudet
def routtle(q, population : List[str]):
  def get_individual(r):
    for i in range(POP_SIZE):
      if r < q[i]:
        return population[i]
    return "0" * M

  new_population = []
  for __ in range(POP_SIZE):
    r = random.random()
    new_population.append(get_individual(r))
  return new_population

# Lựa chọn các cá thể mới
def selection(population : List[str]):
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
  
  new_populate = routtle(q, population)
  return F, max(evals), new_populate


# Lai ghép cá thể
def crossover(population : List[str]):
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
      
  parents = get_parents()
  for i in range(len(parents)):
    pos = random.randint(1, M - 1)
    par1, par2 = population[parents[i][0]], population[parents[i][1]]
    m11, m12 = par1[0 : pos], par1[pos:]
    m21, m22 = par2[0 : pos], par2[pos:]
    new_indi1 = m11 + m22
    new_indi2 = m21 + m12
    population[parents[i][0]] = new_indi1
    population[parents[i][1]] = new_indi2
  
  return population

# print(crossover())
def mutate(population : List[str]):
  total = M * POP_SIZE
  
  for __ in range(total):
    r = random.random()
    if r < MUTATION_PROBABILITY:
      pos = random.randint(1, total)
      # n_chromo * M + n_bit = pos
      n_chromo = math.floor(pos / M)
      n_bit = pos - n_chromo * M

      # Tiến hành mutate
      tmp_bit = population[n_chromo - 1][n_bit]
      if tmp_bit == "1":
        tmp_bit = "0"
      else:
        tmp_bit = "1"
      tmp_string = list(population[n_chromo - 1])
      tmp_string[n_bit - 1] = tmp_bit
      population[n_chromo - 1] = ''.join(tmp_string)    
  
  return population
      
# Thuật toán di truyền
def genetic_algorithm():
  best = 0
  population = initalize()

  for i in range(1, TOTAL_GENERATION + 1):
    F, gtln, population = selection(population)
    print("Thế hệ", i, "có tổng độ thích nghi là:", F, "đạt giá trị hàm f lớn nhất là:", gtln)
    population = crossover(population)
    population = mutate(population)
    best = max(best, gtln)
  
  return best

best = genetic_algorithm()
print("Hàm số f đạt giá trị lớn nhất sau cùng là:", best)