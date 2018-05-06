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


def remove_candidates_row(c, s, i, e, d):
    for j in range(9):
        if (i, j) not in e | d:
            c[i][j] -= s

            
def remove_candidates_col(c, s, j, e, d):
    for i in range(9):
        if (i, j) not in e | d:
            c[i][j] -= s


def square_idx_to_pos(idx):
    return (idx // 3) * 3, (idx % 3) * 3


def pos_to_square_idx(i, j):
    return (i // 3) * 3 + j // 3


def remove_candidates_squ(c, s, idx, e, d):
    ii, ij = square_idx_to_pos(idx)
    for i in range(3):
        for j in range(3):
            ci = ii + i
            cj = ij + j
            if (ci, cj) not in e | d:
                c[ci][cj] -= s


def init_candidates(c, d):
    r = True
    for i in range(9):
        for j in range(9):
            cs = c[i][j]
            if len(cs) < 1:
                r = False
                break 
            if len(cs) == 1:
                set_candidate(c, list(cs)[0], i, j, d)
        if not r:
            break
    return r


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


def get_definitory_lines(c, idx, d):
    ii, ij = square_idx_to_pos(idx)
#    print("gdl idx {}".format(idx))
    rows = {}
    cols = {}
    for i in range(3):
        ci = ii + i
        rs = None
        ps = []
        for j in range(3):
            cj = ij + j
            cs = c[ci][cj]
            assert len(cs) != 1 or (ci, cj) in d, "{} es {}".format((ci, cj), candidate_set_to_str(cs))
            if len(cs) > 1:
                if rs is None:
                    rs = set(cs)
#                print("ci {} cj {} cs {} rs {}".format(ci, cj, candidate_set_to_str(cs), candidate_set_to_str(rs)))
                rs &= cs
                ps.append((ci, cj))
        if rs and check_uniq_definitory_row(c, idx, i, rs):
#            print("g ci {} rs {}".format(ci, candidate_set_to_str(rs)))
            rows[ci] = [rs, set(ps)]
            
#    print("r1 rows {}".format(rows))
    for j in range(3):
        cj = ij + j
        rs = None
        ps = []
        for i in range(3):
            ci = ii + i
            cs = c[ci][cj]
            if len(cs) > 1 or (ci, cj) not in d:
                if rs is None:
                    rs = set(cs)
#                print("ci {} cj {} cs {} rs {}".format(ci, cj, candidate_set_to_str(cs), candidate_set_to_str(rs)))
                rs &= cs
                ps.append((ci, cj))
        if rs and check_uniq_definitory_col(c, idx, j, rs):
#            print("g cj {} rs {}".format(cj, candidate_set_to_str(rs)))
            cols[cj] = [rs, set(ps)]
#    print("r rows {}".format(rows))
#    print("r cols {}".format(cols))
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
                for n in cs:
                    cnt[n] += 1
                    if n not in cntp:
                        cntp[n] = ci, cj
#    print("idx {} p {}".format(idx, cntp))
    r = list(map(itemgetter(0), filter(lambda item:item[1] == 1, cnt.items())))

    return list(zip(r, map(lambda x:cntp[x], r)))


def get_unique_candidates_in_row(c, i, d):
    cnt = dict(zip(map(str, range(1, 10)), [0] * 9))
    cntp = {}
    for j in range(9):
        if (i, j) not in d:
            cs = c[i][j]
            for n in cs:
                cnt[n] += 1
                if n not in cntp:
                    cntp[n] = i, j
#    print("uccr i {} c {} p {}".format(i, cnt, cntp))
    r = list(map(itemgetter(0), filter(lambda item:item[1] == 1, cnt.items())))
#    print("r {}".format(list(map(lambda x:cntp[x], r))))

    return list(zip(r, map(lambda x:cntp[x], r)))


def get_unique_candidates_in_col(c, j, d):
    cnt = dict(zip(map(str, range(1, 10)), [0] * 9))
    cntp = {}
    for i in range(9):
        if (i, j) not in d:
            cs = c[i][j]
            for n in cs:
                cnt[n] += 1
                if n not in cntp:
                    cntp[n] = i, j
#    print("uccc j {} c {} p {}".format(j, cnt, cntp))
    r = list(map(lambda n:(n[0], cntp[n[0]]), filter(lambda item:item[1] == 1, cnt.items())))

    return r


def set_candidate(c, n, i, j, d):
    idx = pos_to_square_idx(i, j)
    cs = set([n])
    p = (i, j)
    e = set([p])
    remove_candidates_row(c, cs, i, e, d)
    remove_candidates_col(c, cs, j, e, d)
    remove_candidates_squ(c, cs, idx, e, d)
    d.add(p)
    c[i][j] = cs


def process_unique_candidates(c, d):
    rows = []
    cols = []
    squares = []
    for i in range(9):
        rowst = get_unique_candidates_in_row(c, i, d)
        rows.extend(rowst)
    
    print("uc rows {}".format(rows))
    
    for n, (i, j) in rows:
#        print("pon n {} p {}".format(n, (i, j)))
        set_candidate(c, n, i, j, d)
        
    print(candidates_to_str(c))

    for j in range(9):
        colst = get_unique_candidates_in_col(c, j, d)
        cols.extend(colst)
        
    print("uc cols {}".format(cols))

    for n, (i, j) in cols:
        set_candidate(c, n, i, j, d)
        
    print(candidates_to_str(c))
        
    for idx in range(9):
        squrest = get_unique_candidates_in_square(c, idx, d)
        squares.extend(squrest)

    print("uc sqs {}".format(squares))
    
    for n, (i, j) in squares:
        set_candidate(c, n, i, j, d)
        
    print(candidates_to_str(c))
        
    return (not not rows) or cols or squares


def process_definitory_lines(c, d):
    rows = {}
    cols = {}
    for i in range(9):
        rows[i] = []
        cols[i] = []
    for idx in range(9):
        rowst, colst = get_definitory_lines(c, idx, d)
#        print(" idx {} r {} c {}".format(idx, list(map(lambda x:candidate_set_to_str(rowst[x][0]) + ":" + str(rowst[x][1]), rowst)), list(map(lambda x:candidate_set_to_str(colst[x][0]) + ":" + str(colst[x][1]), colst))))
        for i in rowst:
            print("dl en i {} se anade {}".format(i, rowst[i]))
            rows[i].append(rowst[i])
        for j in colst:
            cols[j].append(colst[j])
#            print("dl en j {} se anade {} aora es {}".format(j, colst[j], cols[j]))
    
    print("dl r {} c {}".format(rows, cols))
#    print("dl  r {} c {}".format(list(map(lambda x:candidate_set_to_str(rows[x][0]) + ":" + str(rows[x][1]), rows)), list(map(lambda x:candidate_set_to_str(cols[x][0]) + ":" + str(cols[x][1]), cols))))
    for i in rows:
        for s, e in rows[i]:
#        print("cara {}".format(e))
            remove_candidates_row(c, s, i, e, d)
        
    print("removed dl from rows")
    print(candidates_to_str(c))
    
    print("proc uniq en cand r")
    process_uniques_in_candidate_set(c, d)
    
    for j in cols:
        for s, e in cols[j]:
            remove_candidates_col(c, s, j, e, d)
    
    process_uniques_in_candidate_set(c, d)
    print("removed dl from cols")
    print(candidates_to_str(c))
    
    print("proc uniq en cand c")
    process_uniques_in_candidate_set(c, d)
    
    return (not not rows) or cols

    
def candidates_sol_to_str(c):
    r = []
    for i in range(9):
        rt = []
        for j in range(9):
            cs = c[i][j]
            if len(cs) == 1:
                rt += [str(list(cs)[0])]
            else:
                rt += candidate_set_to_str(cs)
        r.append(rt)
    return "\n".join(map(lambda l:"|".join(l), r))


def candidate_sol_write_to_board(c, board):
    for i in range(9):
        for j in range(9):
            cs = c[i][j]
            assert len(cs) == 1, "fucj {}".format(cs)
            board[i][j] = list(cs)[0]


def check_candidates_complete(c):
    r = True
    for i in range(9):
        for j in range(9):
            cs = c[i][j]
            if len(cs) != 1:
                r = False
                break
        if not r:
            break
    return r

            
def process_uniques_in_candidate_set(c, d):
    r = False
    for i in range(9):
        for j in range(9):
            cs = c[i][j]
            if len(cs) == 1 and (i, j) not in d:
                n = list(cs)[0]
                set_candidate(c, n, i, j, d)
                r = True
    return r


class Solution:

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        print("board {}".format(board))
        d = set()
        c = create_candidates(board)
        print("original")
        print(candidates_to_str(c))
        v = init_candidates(c, d)
        print("inited")
        print(candidates_to_str(c))
        while(process_uniques_in_candidate_set(c, d)):
            pass
        print("inited unicos ")
        print(candidates_to_str(c))
        while v:
            print("process def lines")
            pd = process_definitory_lines(c, d)
            print("process uniq in cand")
            while(process_uniques_in_candidate_set(c, d)):
                pass
            print("process uniq lines")
            pu = process_unique_candidates(c, d)
            print("process uniq in cand")
            while(process_uniques_in_candidate_set(c, d)):
                pass
            if not pd and not pu:
                break
        if check_candidates_complete(c):
            print("vien")
        else:
            print("fick")
        print("{}".format(candidates_sol_to_str(c)))
        # candidate_sol_write_to_board(c, board)
        print(board)


m = []


for _ in range(9):


    m.append(list(input().strip()))

s = Solution()
s.solveSudoku(m)
