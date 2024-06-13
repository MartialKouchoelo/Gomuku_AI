#!/bin/python3
import sys
import random

def nb_bits(nb) -> int:
    r = 0
    tmp = max(nb)
    if tmp != nb[0]:
        tmp = min(nb)
    if tmp == 0:
        tmp = 1
    while tmp != 0:
        r+=1
        tmp >>= 1
    return r

class _ai:
    winpatterns = {tuple([15]): [(-1, 0), (4, 0)],
                    (1, 1, 1, 1): [(0, -1), (0, 4)],
                    (8, 4, 2, 1): [(-1, -1), (4, 4)],
                    (1, 2, 4, 8): [(1, -1), (-4, 4)],
                    tuple([23]): [(1,0)],
                    (16,0,4,2,1): [(1,1)],
                    (1,0,1,1,1): [(0,1)],
                    (1,0,4,8,16): [(-1,1)],
                    tuple([29]): [(3,0)],
                    (16,8,4,0,1): [(3,3)],
                    (1,1,1,0,1): [(0,3)],
                    (1,2,4,0,16): [(-3,3)],
                    tuple([27]): [(2,0)],
                    (16,8,0,2,1): [(2,2)],
                    (1,1,0,1,1): [(0,2)],
                    (1,2,0,8,16): [(-2,2)]
                }
    warnpatterns = {tuple([7]): [(-1, 0), (3, 0)],
                    (1, 1, 1): [(0, -1), (0, 3)],
                    (4, 2, 1): [(-1, -1), (3, 3)],
                    (1, 2, 4): [(1, -1), (-3, 3)],
                    (6,1,1): [(2,0)],
                    (1,1,6): [(0,2)],
                    (3,4,4): [(-1, 0)],
                    (4,4,3): [(0, 2)],
                    (2,1,0,1,2): [(2,2)],
                    (1,2,0,2,1): [(-2,2)],
                    (10,17): [(1,-1)],
                    (9,2): [(2,0)],
                    (17,10): [(2,2)],
                    (5,2,2): [(1,0)],
                    (2,2,5): [(0,2)],
                    (2,5,2): [(1,1)],
                    (5,0,5): [(1,1)],
                    (1,6,1): [(0, 1)],
                    (4,3,4): [(0,1)],
                    (4,0,5,8): [(1,1)],
                    (2,0,10,1): [(-1,1)],
                    (8,5,0,4): [(2,2)],
                    (1,10,0,2): [(-2,2)],
                    (1,1,0,1): [(0,2)],
                    (1,0,1,1): [(0,1)],
                    tuple([11]): [(1,0)],
                    tuple([13]): [(2,0)],
                    (8,4,0,1): [(2,2)],
                    (8,0,2,1): [(1,1)],
                    (1,2,0,8): [(-2,2)],
                    (1,0,4,8): [(-1,1)],
                    (2,5,2): [(0,1)],
                    (5,0,5): [(1,1)]
                }
    third_degree = {tuple([3]): [(-1,0), (2,0)],
                    (5,2): [(1,2)],
                    tuple([5]): [(1,0)],
                    (1,2): [(2,-1), (-1,2)],
                    (1,0,4): [(-1,3), (3,-1), (-1,2)],
                    (2,1): [(-1,-1), (2,2)],
                    (4,0,1): [(1,1), (-1,-1), (3,3)],
                    (1,1): [(0,2), (0,-1), (0,3), (0,-2)],
                    (1,0,1): [(0,1), (0,3), (0,-1)]
        }
    second_degree = {tuple([1]): [(1,0), (0,1), (-1,0), (0,-1), (-1,-1), (1,1), (-1,1), (1,-1), (0,2), (2,0), (-2,0), (0,-2), (2,2), (-2,-2), (2,-2), (-2,2)]}
    def __init__(self) -> None:
        pass

    def convert_goban(self, goban):
        listp = []
        listai = []

        for i in range(0, len(goban)):
            nb_p = 0
            nb_ai = 0
            for j in range(0, len(goban)):
                if goban[i][j] == 'o':
                    nb_p ^= (1 << 19) >> j
                elif goban[i][j] == 'x':
                    nb_ai ^= (1 << 19) >> j
            listp.append(nb_p)
            listai.append(nb_ai)

        return listp,listai

    def check_supperpose(self, Turnlist, posx, posy, patterncheck) -> bool:
        nb = len(patterncheck)
        nbits = nb_bits(patterncheck)
        for i in range(0, nb):
            #print("{0:020b}".format(Turnlist[posx+i] << (posy)))
            #print("{0:020b}".format((patterncheck[i] << (20 + posy - nb_bits(patterncheck)))))
            if (i > 19 - posx):
                return False
            if ((Turnlist[posx + i] << (posy)) != ((patterncheck[i] << (20 - nbits)) | (Turnlist[posx + i] << (posy)))):
                return False
        return True

    def display_board(self, goban):
        posx = 0
        posy = 0
        lstp,lstai = self.convert_goban(goban)
        print("player              |ai")
        for x in range(len(lstp)):
            print("{0:020b}".format(lstp[x]), end="|")
            print("{0:020b}".format(lstai[x]), end="")
            print("")

    def compute(self, goban, pstones, aistones):
        if len(aistones) > 0 or len(pstones) > 0:
            lstp,lstai = self.convert_goban(goban)
        #win if possible
        if len(aistones) != 0:
            for pos in aistones:
                yy, xx = pos[1], pos[0]
                for pattern in self.winpatterns.keys():
                    if(self.check_supperpose(lstai,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.winpatterns[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        #block defeat
        if len(pstones) != 0:
            for pos in pstones:
                yy, xx = pos[1], pos[0]
                for pattern in self.winpatterns.keys():
                    if(self.check_supperpose(lstp,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.winpatterns[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        #attack 4th_degree
        if len(aistones) != 0:
            for pos in aistones:
                yy, xx = pos[1], pos[0]
                for pattern in self.warnpatterns.keys():
                    if(self.check_supperpose(lstai,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.warnpatterns[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        #defense 4th_degree
        if len(pstones) != 0:
            for pos in pstones:
                yy, xx = pos[1], pos[0]
                for pattern in self.warnpatterns.keys():
                    if(self.check_supperpose(lstp,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.warnpatterns[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        #attack 3th_degree
        if len(aistones) != 0:
            for pos in aistones:
                yy, xx = pos[1], pos[0]
                for pattern in self.third_degree.keys():
                    if(self.check_supperpose(lstai,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.third_degree[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        #attack 2nd_degree
        if len(aistones) != 0:
            for pos in aistones:
                yy, xx = pos[1], pos[0]
                for pattern in self.second_degree.keys():
                    if(self.check_supperpose(lstai,yy,xx,pattern)):
                        #print(xx, yy, pattern)
                        for block in self.second_degree[pattern]:
                            try:
                                mark = goban[yy+block[1]][xx+block[0]]
                            except(IndexError):
                                continue
                            if mark != '0':
                                continue
                            if yy+block[1] < 0 or xx+block[0] < 0:
                                continue
                            return xx+block[0],yy+block[1]
        posx = random.randint(0, len(goban)-1)
        posy = random.randint(0, len(goban)-1)
        while goban[posy][posx] != '0':
            posx = random.randint(0, len(goban)-1)
            posy = random.randint(0, len(goban)-1)
        return posx,posy