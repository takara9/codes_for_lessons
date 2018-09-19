#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import math
np.set_printoptions(threshold='nan')

# 素数判定関数
def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))

# 素数生成関数
def prime_number_generater(nstart, nsize):
    nend = nstart + nsize
    ay   = np.arange(nstart, nend)
    # 素数判定の関数をベクタ化
    pvec = np.vectorize(is_prime)
    # 配列要素へ適用して判定表
    primes_t = pvec(ay)
    # 素数だけを抽出して表示
    primes = np.extract(primes_t, ay)
    return primes

if __name__ == '__main__':
    p = sys.stdin.read().split(",")
    print p
    print prime_number_generater(int(p[0]),int(p[1]))
    

