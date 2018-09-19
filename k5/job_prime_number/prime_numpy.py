#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import math
np.set_printoptions(threshold='nan')


# 素数判定関数
def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


# 配列の中に１から順に数字を並べる
nstart = eval(os.environ.get("A_START_NUM"))
nsize  = eval(os.environ.get("A_SIZE_NUM"))
nend   = nstart + nsize
ay     = np.arange(nstart, nend)

# 素数判定の関数をベクタ化
pvec = np.vectorize(is_prime)

# 配列要素へ適用して判定表
primes_tf = pvec(ay)

# 素数だけを抽出して表示
primes = np.extract(primes_tf, ay)
print primes


