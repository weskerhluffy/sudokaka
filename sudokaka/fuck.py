'''
Created on 05/05/2018

@author: ernesto
'''


def create_candidates(m):
    c = []
    for i in range(9):
        c.append([])
        for j in range(9):
            if m[i][j] != '.':
                ns = set([m[i][j]])
            else:
                ns = set(map(str, range(1, 10)))    
#            print("ns {}".format(candidate_set_to_str(ns)))
            c[-1].append(ns)
    return c


def remove_candidates_row(c, s, i, e):
    for j in range(9):
        if (i, j) not in e:
            c[i][j] -= s

            
def remove_candidates_col(c, s, j, e):
    for i in range(9):
        if (i, j) not in e:
            c[i][j] -= s


def square_idx_to_pos(idx):
    return (idx // 3) * 3, (idx % 3) * 3


def pos_to_square_idx(i, j):
    return (i // 3) * 3 + j // 3


def remove_candidates_squ(c, s, idx, e):
    ii, ij = square_idx_to_pos(idx)
    for i in range(3):
        for j in range(3):
            ci = ii + i
            cj = ij + j
            if (ci, cj) not in e:
                c[ci][cj] -= s


def init_candidates(c):
    for i in range(9):
        for j in range(9):
            p = i, j
            idx = pos_to_square_idx(i, j)
            e = set([p])
            cs = c[i][j]
            assert len(cs) > 0
            if len(cs) == 1:
                remove_candidates_row(c, cs, i, e)
                remove_candidates_col(c, cs, j, e)
                remove_candidates_squ(c, cs, idx, e)


def candidate_set_to_str(cs):
    r = []
    for i in range(1, 10):
        cc = "-"
        if str(i) in cs:
            cc = str(i)
        r.append(cc)
    return ",".join(r)


def candidates_to_str(c):
    r = []
    for i in range(9):
        rt = []
        for j in range(9):
            cs = c[i][j]
            rt.append(candidate_set_to_str(cs))
        r.append("|".join(rt))
    return "\n".join(r)


class Solution:

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        c = create_candidates(board)
        init_candidates(c)
        print(candidates_to_str(c))


m = []


for _ in range(9):
    m.append(input().strip())

s = Solution()
s.solveSudoku(m)
