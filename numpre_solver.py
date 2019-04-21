#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os.path
import math

cnf = [] # cnfは一行ずつ取っておく．

# 数独の問題ファイルをcnfに変換する．
def convert_cnf(name):
    arr = []

    # 問題ファイルより問題を読み取る．
    for line in open(name, 'r'):
        str_row = (line[:-1].split(','))
        row = []
        for s in str_row:
            if s == "-":
                row.append(int(0))
            else:
                row.append(int(s))
        arr.append(row)

    row_length = len(row)
    column_length = len(arr)

    # 正方形なのか確認
    if row_length == column_length:
        n = int(math.sqrt(row_length))
    else:
        return -1

    # 問題の情報を返す．
    print("  square number plate problem : " + str(n) + "^2")
    print("  [pazzle problems]")
    print("    _____________________")
    for i in range(len(arr)):
        print("    |"),
        for j in range(len(arr[i])):
            if arr[i][j] != 0:
                print(str(arr[i][j])),
            else:
                print("-"),
        print("|")
    print("    _____________________")

    list = []

    # 各マスに関するリテラル
    for i in range(n**2):
        for j in range(n**2):
            tmp_list = []
            for k in range(n**2):
                tmp_list.append(i*(n**4) + j*(n**2) + k + 1)
            list.append(tmp_list)

    # 各行に関するリテラル
    for i in range(n**2):
        for j in range(n**2):
            tmp_list = []
            for k in range(n**2):
                tmp_list.append(i + j*(n**4) + k*(n**2) + 1)
            list.append(tmp_list)

    # 各列に関するリテラル
    for i in range(n**2):
        for j in range(n**2):
            tmp_list = []
            for k in range(n**2):
                tmp_list.append(i + j*(n**2) + k*(n**4) + 1)
            list.append(tmp_list)

    # 各ブロックに関するリテラル
    for i in range(n**2):
        for j in range(n**2):
            tmp_list = []
            for k in range(n*n):
                tmp_list.append(i + (j%n)*(n**3) + int(j/n)*(n**5) + (k%n)*(n**2) + int(k/n)*(n**4) + 1)
            list.append(tmp_list)

    # 各マス，行，列，ブロックに同じ数字がひとつ以上現れる． (at-least-one制約)
    for i in list:
        s = ""
        for j in i:
            s += str(j) + " "
        s += str(0)
        cnf.append(s)

    # 各マス，行，列，ブロックに入る同じ数字はたかだかひとつである． (at-most-one制約)
    for i in range(len(list)):
        pairwise(list[i])

    # 数字の埋まっているマスの情報を書き込む．
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] != 0:
                cnf.append(str(i*(n**4) + j*(n**2) + arr[i][j]) + " 0")

    cnf_number = len(cnf)
    cnf.insert(0, "p cnf " + str(n**6) + " " + str(cnf_number))

    root, ext = os.path.splitext(name)

    with open(root + '.cnf', mode='w') as f:
        for s in cnf:
            f.write(s + '\n')
        f.close()

    return n

# at-most-one制約はpairwise法で記述する．
def pairwise(l):
    if len(l) < 2:
        return
    for j in range(len(l)-1):
        cnf.append("-" + str(l[0]) + " -" + str(l[j+1]) + " 0")
    l.pop(0)
    return pairwise(l)

# solverのlogを解析して，答えを出力
def analysis_log(name, n):

    # logを読み取る．
    log_list = []
    for line in open(name, 'r'):
        if line.startswith("v"):
            line[1:]
            log_list += line[1:].split()
        if line.startswith("c CPU Time"):
            print("  Solving Time" + line[10:])

    log_list_int = [int(s) for s in log_list]
    answer = []

    for i in range(len(log_list_int)):
        if log_list_int[i] > 0:
            answer.append(log_list_int[i])

    # 出力
    print("   [pazzle answer]")
    print("   _____________________")
    for i in range(n**2):
        print("   |"),
        for j in range(n**2):
            if i == 0:
                if answer[j + i*(n**2)] % (n**2) == 0:
                    print(9),
                else:
                    print(str(answer[j + i*(n**2)] % (n**2))),
            else:
                print(str(answer[j + i*(n**2)] % (j*(n**2) + i*(n**4)))),
        print("|")
    print("   _____________________")



def run_and_capture(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = []

    while True:

        line = proc.stdout.readline()
        buf.append(line)
        sys.stdout.write(line)

        if not line and proc.poll() is not None:
            break

    return ''.join(buf)

if __name__ == '__main__':
    numpre_name = raw_input("解きたい数独問題のパス : ")
    root, ext = os.path.splitext(numpre_name)

    print("********************SAT-based Sudoku Solver********************")
    print("1. Encording")
    n = convert_cnf(numpre_name) # nは数独のサイズ

    print("\n 2. Solving...")
    solver = "clasp" # どのソルバーで解かせるか
    print("   solver :" + solver)
    run_and_capture(solver + " " + root + ".cnf>" + root + ".log")
    print("   solved!")

    print("\n 3. Decording")
    analysis_log(root + ".log", n)
    print("***************************************************************")
