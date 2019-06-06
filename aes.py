import numpy as np
import pprint

def jouzan(bit1, bit2, p):
    jouyo = []

    for i in bit1:
        for k in bit2:
            p1 = np.poly1d([i[0],i[1],i[2]])
            p2 = np.poly1d([k[0],k[1],k[2]])
            jouyo.append((p1*p2/p)[1].coef)
    retu = ""
    li = []
    result = []
    for i, j in enumerate(jouyo):
        j = j.tolist()
        j = map(round, j)
        j = list(map(str, j))
        new_j = []
        for num in j:
            s = ""
            if num == "2" or num == '-2':
                s = '0'
            elif num == '-1' or num == '-3':
                s = '1'
            else:
                s = num
            new_j.append(s)
        li.append(int("".join(new_j), 2))
        if (i+1) % 8 == 0 and i != 0:
            result.append(li)
            li = []
    return result

def s_box(a):
    if a == 0:
        return 1
    elif a == 1:
        return 2
    elif a == 2:
        return 6
    elif a == 3:
        return 3
    elif a == 4:
        return 0
    elif a == 5:
        return 7
    elif a == 6:
        return 4
    elif a == 7:
        return 5

def add_key(M, K):
    new_M = []
    for i in range(4):
        row = []
        for k in range(4):
            row.append(int(M[i][k]^K[i][k]))
        new_M.append(row)
    print('--------AddRoundKey--------')
    pprint.pprint(new_M)
    return new_M

def sub_bytes(M):
    new_M = []
    for i in range(4):
        row = []
        for k in range(4):
            row.append(s_box(M[i][k]))
        new_M.append(row)
    print('--------SubBytes--------')
    pprint.pprint(new_M)
    return new_M

def shift_rows(M):
    M[1][0], M[1][1], M[1][2], M[1][3] = M[1][1], M[1][2], M[1][3], M[1][0]
    M[2][0], M[2][1], M[2][2], M[2][3] = M[2][2], M[2][3], M[2][0], M[2][1]
    M[3][0], M[3][1], M[3][2], M[3][3] = M[3][3], M[3][0], M[3][1], M[3][2]
    print('--------Shift_rows--------')
    pprint.pprint(M)
    return M

def mix_columns(M, jouzan_list): #jouzan_listはa･bの二次元配列
    new_M = [[0 for i in range(4)] for j in range(4)]
    A = [[2,3,1,1], [1,2,3,1], [1,1,2,3],[3,1,1,2]]
    for i in range(4):
        column = [c[i] for c in M]
        for index, a in enumerate(A):
            new_M[index][i] = int(jouzan_list[column[0]][a[0]] ^ jouzan_list[column[1]][a[1]] ^ jouzan_list[column[2]][a[2]] ^ jouzan_list[column[3]][a[3]])
    print('--------MixColumns--------')
    pprint.pprint(new_M)
    return new_M

def key_schedule(K, i):
    beki = [1, 2, 4, 3, 6, 7, 5, 1, 2, 4, 3]
    rc = beki[i]
    new_K = [[0 for i in range(4)] for j in range(4)]
    r = [c[3] for c in K]
    r[0],r[1],r[2],r[3] = r[1],r[2],r[3],r[0]
    new_r = []
    for i in range(4):
        new_r.append(s_box(r[i]))
    new_r[0] = int(new_r[0] ^ rc)
    column = [c[0] for c in K]
    a = [0 for i in range(4)]
    for i in range(4):
        new_K[i][0] = int(column[i] ^ new_r[i])
        a[i] = new_K[i][0]
    for k in range(3):
        column = [c[k+1] for c in K]
        for i in range(4):
            new_K[i][k+1] = int(column[i] ^ a[i])
            a[i] = new_K[i][k+1]
    print('--------KeySchedule--------')
    pprint.pprint(new_K)
    return new_K

def main():
    n = 9
    M = [[3,3,3,3],[3,3,3,3],[3,3,3,3],[3,3,3,3]]
    K = [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]
    bit1 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
    bit2 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
    p = np.poly1d([1,0,1,1])
    M = add_key(M, K)
    for i in range(n):
        print('==========================={}回目==========================='.format(i+1))
        M = sub_bytes(M)
        M = shift_rows(M)
        M = mix_columns(M, jouzan(bit1, bit2, p))
        K = key_schedule(K, i)
        M = add_key(M, K)
    print('===========================10回目===========================')
    M = sub_bytes(M)
    M = shift_rows(M)
    M = add_key(M, K)

if __name__ == '__main__':
    main()
