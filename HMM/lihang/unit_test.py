#! /usr/bin/env python
# ! -*- coding=utf-8 -*-
from hmm import *
import numpy as np
import pandas as pd


def test_e101():
    logger.info("Exercise 10.1")
    raw_data = pd.read_csv("./Input/data_10-1.txt", header=0, index_col=0)
    # print(raw_data)
    # print(list(raw_data.columns), list(raw_data.index))
    O = [0, 0, 1, 1, 0]
    # 以上为已知
    T = len(O)
    Q = set(raw_data.columns[-1 - len(raw_data):-1])
    N = len(Q)
    V = set(raw_data.columns[:-1 - len(raw_data)])
    M = len(V)
    A = raw_data[raw_data.columns[-1 - len(raw_data):-1]].values
    B = raw_data[raw_data.columns[:-1 - len(raw_data)]].values
    B = B / np.sum(B, axis=1).reshape((-1, 1))

    if raw_data[["pi"]].apply(np.isnan).values.flatten().sum() > 1:
        pi = [1 / raw_data[["pi"]].apply(np.isnan).values.flatten().sum()] * N
    print("\nT\n%s\nA\n%s\nB\n%s\npi\n%s\nM\n%s\nN\n%s\nO\n%s\nQ\n%s\nV\n%s"
          % (T, A, B, pi, M, N, O, Q, V))


def test_e102():
    logger.info("Exercise 10.2")
    raw_data = pd.read_csv("./Input/data_10-2.txt", header=0, index_col=0, na_values="None")
    O = [0, 1, 0]
    # 以上为已知
    T = len(O)
    Q = set(raw_data.columns[-1 - len(raw_data):-1])
    N = len(Q)
    V = set(raw_data.columns[:-1 - len(raw_data)])
    M = len(V)
    A = raw_data[raw_data.columns[-1 - len(raw_data):-1]].values
    B = raw_data[raw_data.columns[:-1 - len(raw_data)]].values
    B = B / np.sum(B, axis=1).reshape((-1, 1))

    if raw_data[["pi"]].apply(np.isnan).values.flatten().sum() > 1:
        pi = [raw_data[["pi"]].apply(np.isnan).values.flatten().sum()] * N
    else:
        pi = raw_data[["pi"]].values.flatten()
    logger.info("\nT\n%s\nA\n%s\nB\n%s\npi\n%s\nM\n%s\nN\n%s\nO\n%s\nQ\n%s\nV\n%s"
                % (T, A, B, pi, M, N, O, Q, V))
    # forward
    print(pi * B[..., O[0]])
    print(np.dot(pi * B[..., O[0]], A) * B[..., O[1]])
    print(np.dot(np.dot(pi * B[..., O[0]], A) * B[..., O[1]], A) * B[..., O[2]])
    print(np.sum(np.dot(np.dot(pi * B[..., O[0]], A) * B[..., O[1]], A) * B[..., O[2]]))
    # backward
    print(np.dot(A, B[..., O[2]]))


def test_e103():
    raw_data = pd.read_csv("./Input/data_10-2.txt", header=0, index_col=0, na_values="None")
    O = [0, 1, 0]
    # 以上为已知
    T = len(O)
    Q = set(raw_data.columns[-1 - len(raw_data):-1])
    N = len(Q)
    V = set(raw_data.columns[:-1 - len(raw_data)])
    M = len(V)
    A = raw_data[raw_data.columns[-1 - len(raw_data):-1]].values
    B = raw_data[raw_data.columns[:-1 - len(raw_data)]].values
    B = B / np.sum(B, axis=1).reshape((-1, 1))

    if raw_data[["pi"]].apply(np.isnan).values.flatten().sum() > 1:
        pi = [raw_data[["pi"]].apply(np.isnan).values.flatten().sum()] * N
    else:
        pi = raw_data[["pi"]].values.flatten()
    print("\nT\n%s\nA\n%s\nB\n%s\npi\n%s\nM\n%s\nN\n%s\nO\n%s\nQ\n%s\nV\n%s"
          % (T, A, B, pi, M, N, O, Q, V))
    hmm_e103 = HMM(n_component=3)
    hmm_e103.A = A
    hmm_e103.B = B
    hmm_e103.p = pi
    hmm_e103.N = N
    hmm_e103.T = T
    hmm_e103.M = M

    prob, states = hmm_e103.decode(O)
    print("P star is %s, I star is %s" % (prob, states))
    # print("参考答案")
    # print(np.array([[0.1,     0.028,   0.00756],
    #                 [0.016,   0.0504,  0.01008],
    #                 [0.28,    0.042,   0.0147]]))
    # print("程序结果")
    # print(delta)


def test_forward():
    # 10.2 数据
    Q = {0: 1, 1: 2, 2: 3}
    V = {0: "red", 1: "white"}
    hmm_forward = HMM(n_component=3)
    hmm_forward.A = np.array([[0.5, 0.2, 0.3],
                              [0.3, 0.5, 0.2],
                              [0.2, 0.3, 0.5]])
    hmm_forward.B = np.array([[0.5, 0.5],
                              [0.4, 0.6],
                              [0.7, 0.3]])
    hmm_forward.p = np.array([0.2, 0.4, 0.4])
    X = np.array([0, 1, 0])
    hmm_forward.T = len(X)

    prob, alpha = hmm_forward._do_forward(X)
    alpha_true = np.array([[0.10, 0.077, 0.04187],
                           [0.16, 0.1104, 0.03551],
                           [0.28, 0.0606, 0.05284]])


def test_backward():
    # 10.2 数据
    Q = {0: 1, 1: 2, 2: 3}
    V = {0: "red", 1: "white"}
    hmm_backward = HMM(n_component=3)
    hmm_backward.A = np.array([[0.5, 0.2, 0.3],
                               [0.3, 0.5, 0.2],
                               [0.2, 0.3, 0.5]])
    hmm_backward.B = np.array([[0.5, 0.5],
                               [0.4, 0.6],
                               [0.7, 0.3]])
    hmm_backward.p = np.array([0.2, 0.4, 0.4])
    X = np.array([0, 1, 0])
    hmm_backward.T = len(X)

    prob, alpha = hmm_backward._do_backward(X)
    alpha_true = np.array([[0.10, 0.077, 0.04187],
                           [0.16, 0.1104, 0.03551],
                           [0.28, 0.0606, 0.05284]])


def test_bkw_frw():
    # 并没有实际的测试内容
    Q = {0: 1, 1: 2, 2: 3}
    V = {0: "red", 1: "white"}
    hmm_forward = HMM(n_component=3)
    hmm_forward.A = np.array([[0.5, 0.2, 0.3],
                              [0.3, 0.5, 0.2],
                              [0.2, 0.3, 0.5]])
    hmm_forward.B = np.array([[0.5, 0.5],
                              [0.4, 0.6],
                              [0.7, 0.3]])
    hmm_forward.p = np.array([0.2, 0.4, 0.4])
    X = np.array([0, 1, 0])
    hmm_forward.T = len(X)

    beta = hmm_forward.backward(X)
    alpha = hmm_forward.forward(X)
    print("%s \n %s" % (alpha, beta))


def test_EM():
    logger.info("test EM")
    V = {0: "red", 1: "white"}
    hmm_fit = HMM(n_component=3, V=V)
    X = np.array([0, 1, 0, 0])
    hmm_fit.fit(X)
    # prob, states = hmm_fit.decode([0, 1, 0, 0])
    print(hmm_fit.A)
    print(hmm_fit.B)
    print(hmm_fit.p)


def test_q101():
    # 和 backward结果一致
    # 10.1
    Q = {0: 1, 1: 2, 2: 3}
    V = {0: "red", 1: "white"}
    hmm_backward = HMM(n_component=3, V=V)
    hmm_backward.A = np.array([[0.5, 0.2, 0.3],
                               [0.3, 0.5, 0.2],
                               [0.2, 0.3, 0.5]])
    hmm_backward.B = np.array([[0.5, 0.5],
                               [0.4, 0.6],
                               [0.7, 0.3]])
    hmm_backward.p = np.array([0.2, 0.4, 0.4])
    X = np.array([0, 1, 0, 1])
    hmm_backward.T = len(X)

    # beta = hmm_backward.backward(X)
    prob, beta = hmm_backward._do_backward(X)
    print("----q101----")
    print(prob)
    print(beta)
    # alpha_true = np.array([[0.10, 0.077, 0.04187],
    #                        [0.16, 0.1104, 0.03551],
    #                        [0.28, 0.0606, 0.05284]])
    # self.assertAlmostEqual(prob, 0.13022, places=5)


def test_q102():
    # 10.2
    Q = {0: 1, 1: 2, 2: 3}
    V = {0: "red", 1: "white"}
    hmm_backward = HMM(n_component=3, V=V)
    hmm_backward.A = np.array([[0.5, 0.1, 0.4],
                               [0.3, 0.5, 0.2],
                               [0.2, 0.2, 0.6]])
    hmm_backward.B = np.array([[0.5, 0.5],
                               [0.4, 0.6],
                               [0.7, 0.3]])
    hmm_backward.p = np.array([0.2, 0.3, 0.5])
    X = np.array([0, 1, 0, 0, 1, 0, 1, 1])
    hmm_backward.T = len(X)
    prob, states = hmm_backward.decode(X)
    prob_fwd, _ = hmm_backward._do_forward(X)
    prob_bwd, _ = hmm_backward._do_backward(X)
    print("decode prob %s, forward prob %s, backward prob %s" % (prob, prob_fwd, prob_bwd))
    print(states)
    print("alpha\n %s" % hmm_backward.alpha)
    print("beta\n%s" % hmm_backward.beta)
    print("delta\n%s" % hmm_backward.delta)


def test_q103():
    # 10.3
    Q = {0: 1, 1: 2, 2: 3, 3: 4}
    V = {0: "red", 1: "white"}
    hmm_backward = HMM(n_component=4, V=V)
    hmm_backward.A = np.array([[0, 1, 0, 0],
                               [0.4, 0, 0.6, 0],
                               [0, 0.4, 0, 0.6],
                               [0, 0, 0.5, 0.5]])
    hmm_backward.B = np.array([[0.5, 0.5],
                               [0.3, 0.7],
                               [0.6, 0.4],
                               [0.8, 0.2]])
    hmm_backward.p = np.array([0.25, 0.25, 0.25, 0.25])
    X = np.array([0, 0, 1, 1, 0])
    hmm_backward.T = len(X)

    prob, states = hmm_backward.decode(X)
    prob_fwd, _ = hmm_backward._do_forward(X)
    prob_bwd, _ = hmm_backward._do_backward(X)
    print("----q103----")
    print("decode prob %s, forward prob %s, backward prob %s" % (prob, prob_fwd, prob_bwd))
    print(states)
    print("alpha\n %s" % hmm_backward.alpha)
    print("beta\n%s" % hmm_backward.beta)
    print("delta\n%s" % hmm_backward.delta)


if __name__ == '__main__':
    test_q103()
