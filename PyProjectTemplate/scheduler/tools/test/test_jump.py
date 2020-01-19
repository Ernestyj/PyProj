# -*- coding: utf-8 -*-
import unittest


# def solution(A):
#     # write your code in Python 3.6
#     N = len(A)
#     for i in range(N):
#         while 1 <= A[i] and A[i] <= N and A[i] != A[A[i] - 1]:  # i: i+1
#             pos = A[i] - 1
#             tmp = A[i]
#             A[i] = A[pos]
#             A[pos] = tmp
#             # A[i], A[pos] = A[pos], A[i]
#     for i in range(N):
#         if A[i] != i + 1:
#             return i + 1
#     return N + 1


def solution1(A, B):
    # write your code in Python 3.6
    intervals = list(zip(A, B))
    if len(intervals) == 0:
        return 0
    intervals.sort(key=lambda e: e[0])
    res = []
    res.append(intervals[0])
    for i in range(1, len(intervals)):
        if res[-1][1] < intervals[i][0]:
            res.append(intervals[i])
        else:
            a, b = res[-1]
            res[-1] = (a, max(intervals[i][1], b))
    return len(res)


"""
root r-x delete-this.xls\n root r-- bug-report.pdf\n root r-- doc.xls\n root r-- podcast.flac\n alice r-- system.xls\n root --x invoices.pdf\n admin rwx SETUP.PY
"""
"""
root r-x delete-this.xls
root r-- bug-report.pdf
root r-- doc.xls
root r-- podcast.flac
alice r-- system.xls
root --x invoices.pdf
admin rwx SETUP.PY
"""


def solution(S):
    # write your code in Python 3.6
    lines = S.split("\n")

    minValidLen = 256

    for line in lines:
        if line == "": continue

        owner = line[:6]
        access = line[7:10]
        name = line[11:]
        # print(owner + "|" + access + "|" + name)

        # owner should be root
        if owner != "  root": continue  # cases of " root " should be excluded
        # access should be r-x or r--
        if access[0] != "r" or access[1] == "w": continue
        # ext should be .doc .xls .pdf
        for ext in [".doc", ".xls", ".pdf"]:    # cases of ".doc " should be excluded
            if name.endswith(ext):
                minValidLen = min(minValidLen, len(name))

    return str(minValidLen) if minValidLen != 256 else "NO FILES"


class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("**************************************** setUpClass ****************************************")

    @classmethod
    def tearDownClass(cls):
        print("************************************** tearDownClass ***************************************")

    def setUp(self):
        print("****** setUp *******")

    def tearDown(self):
        print("***** tearDown *****")

    def _example(self):
        print("This is a test example.")

    # def _A(self):
    #     print(solution([1, 3, 6, 4, 1, 2]))

    # def test_A(self):
    #     print(solution([], []))
    #     print(solution([1,2,8,15], [3,6,10,18]))
    #     print(solution([1, 12, 42, 70, 36, -4, 43, 15], [5, 15, 44, 72, 36, 2, 69, 24]))

    def _A(self):
        S = \
"""
  root r-x delete-this.xls \t\t
  root r-- bug-report.pdf 
  root r-- doc.xls
  root r-- podcast.flac
 alice r-- system.xls
  root --x invoices.pdf
 admin rwx SETUP.PY
"""
        print(solution(S))
        S = \
"""
  root rwx a.txt
  root r-- b.txt
  root --x cccc.doc
  root rwx a.txt
  root r-- b.txt
  root --x c c.doc
  root r-x c c.dOc
  root r-x c_c.dOc
"""
        print(solution(S))
        S = \
"""
  root r-x a:\\n:.doc
"""
        print(solution(S))
        S = \
"""
  root r-x a:\\\\n:.doc
"""
        print(solution(S))
        S = \
"""
  root r-- bug-report.pdf
  root r-- .xls
  root r-- .xls
  root r-x . .doc
"""
        print(solution(S))
        S = \
"""
  root r-- \\n.xls
"""
        print(solution(S))
        S = \
"""
  root r-- \\n.xls 
"""
        print(solution(S))
