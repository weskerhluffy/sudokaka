'''
Created on 05/05/2018

@author: ernesto
'''

from operator import iadd, itemgetter


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


def init_candidates(c, d):
    for i in range(9):
        for j in range(9):
            cs = c[i][j]
            assert len(cs) > 0
            if len(cs) == 1:
                set_candidate(c, cs, i, j, d)


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


def check_uniq_definitory_row(c, idx, ri, rs):
    ii, ij = square_idx_to_pos(idx)
    for i in range(3):
        ci = ii + i
        if i != ri:
            for j in range(3):
                cj = ij + j
                cs = c[ci][cj]
                rs -= cs
                if not rs:
                    break
            if not rs:
                break
    return rs


def check_uniq_definitory_col(c, idx, rj, rs):
    ii, ij = square_idx_to_pos(idx)
    for j in range(3):
        cj = ij + j
        if j != rj:
            for i in range(3):
                ci = ii + i
                cs = c[ci][cj]
                rs -= cs
                if not rs:
                    break
            if not rs:
                break
    return rs 


def get_definitory_lines(c, idx):
    ii, ij = square_idx_to_pos(idx)
    rows = {}
    cols = {}
    for i in range(3):
        ci = ii + i
        rs = None
        ps = []
        for j in range(3):
            cj = ij + j
            cs = c[ci][cj]
            if len(cs) > 1:
                if rs is None:
                    rs = set(cs)
#                print("ci {} cj {} cs {} rs {}".format(ci, cj, candidate_set_to_str(cs), candidate_set_to_str(rs)))
                rs &= cs
                ps.append((ci, cj))
        if rs and check_uniq_definitory_row(c, idx, i, rs) and len(rs) <= len(ps):
#            print("g ci {} rs {}".format(ci, candidate_set_to_str(rs)))
            rows[ci] = [rs, ps]
            
#    print("r1 rows {}".format(rows))
    for j in range(3):
        cj = ij + j
        rs = None
        ps = []
        for i in range(3):
            ci = ii + i
            cs = c[ci][cj]
            if len(cs) > 1:
                if rs is None:
                    rs = set(cs)
                rs &= cs
                ps.append((ci, cj))
        if rs and check_uniq_definitory_col(c, idx, j, rs) and len(rs) <= len(ps):
            cols[cj] = [rs, ps]
#    print("r rows {}".format(rows))
    return rows, cols


def get_unique_candidates_in_square(c, idx, d):
    ii, ij = square_idx_to_pos(idx)
    cnt = dict(zip(map(str, range(1, 10)), [0] * 9))
    cntp = {}
    for i in range(3):
        ci = ii + i
        for j in range(3):
            cj = ij + j
            if (ci, cj) not in d:
                cs = c[ci][cj]
                list(map(lambda n:iadd(cnt[n], 1), cs))
                for n in cs:
                    if n not in cntp:
                        cntp[n] = ci, cj
    r = map(itemgetter(0), filter(lambda item:item[1] == 1, cnt.items()))

    return list(zip(r, map(lambda x:cntp[x], r)))


def get_unique_candidates_in_row(c, i, d):
    cnt = dict(zip(map(str, range(1, 10)), [0] * 9))
    cntp = {}
    for j in range(9):
        if (i, j) not in d:
            cs = c[i][j]
            list(map(lambda n:iadd(cnt[n], 1), cs))
            for n in cs:
                if n not in cntp:
                    cntp[n] = i, j
    r = map(itemgetter(0), filter(lambda item:item[1] == 1, cnt.items()))

    return list(zip(r, map(lambda x:cntp[x], r)))


def get_unique_candidates_in_col(c, j, d):
    cnt = dict(zip(map(str, range(1, 10)), [0] * 9))
    cntp = {}
    for i in range(9):
        if (i, j) not in d:
            cs = c[i][j]
            list(map(lambda n:iadd(cnt[n], 1), cs))
            for n in cs:
                if n not in cntp:
                    cntp[n] = i, j
    r = list(map(lambda n:(n, cntp[n]), filter(lambda item:item[1] == 1, cnt.items())))

    return r


def set_candidate(c, n, i, j, d):
    idx = pos_to_square_idx(i, j)
    cs = set([n])
    p = (i, j)
    e = set(p)
    remove_candidates_row(c, cs, i, e)
    remove_candidates_col(c, cs, j, e)
    remove_candidates_squ(c, cs, idx, e)
    d.add(p)


def process_unique_candidates(c, d):
    rows = []
    cols = []
    squares = []
    for i in range(9):
        rowst = get_unique_candidates_in_row(c, i, d)
        rows.extend(rowst)
    
    for n, (i, j) in rows:
        set_candidate(c, n, i, j, d)

    for j in range(9):
        colst = get_unique_candidates_in_col(c, j, d)
        cols.extend(colst)

    for n, (i, j) in cols:
        set_candidate(c, n, i, j, d)
        
    for idx in range(9):
        squrest = get_unique_candidates_in_square(c, idx, d)
        squares.extend(squrest)

    for n, (i, j) in squares:
        set_candidate(c, n, i, j, d)


def process_definitory_lines(c):
    rows = {}
    cols = {}
    for idx in range(9):
        rowst, colst = get_definitory_lines(c, idx)
        print(" idx {} r {} c {}".format(idx, list(map(lambda x:candidate_set_to_str(rowst[x][0]) + ":" + str(rowst[x][1]), rowst)), list(map(lambda x:candidate_set_to_str(colst[x][0]) + ":" + str(colst[x][1]), colst))))
        rows.update(rowst)
        cols.update(colst)
    
    for i in rows:
        s, e = rows[i]
        remove_candidates_row(c, s, i, e)
    
    for j in cols:
        s, e = cols[j]
        remove_candidates_col(c, s, j, e)
    

class Solution:

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        d = set()
        c = create_candidates(board)
        init_candidates(c, d)
        print(candidates_to_str(c))
        process_definitory_lines(c)
        print(candidates_to_str(c))


m = []


for _ in range(9):
    m.append(input().strip())

s = Solution()
s.solveSudoku(m)
