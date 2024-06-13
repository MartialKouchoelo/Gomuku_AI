#!/bin/python3
import random
import ai

class game:
    def __init__(self):
        self.goban = []
        self.pstones = []
        self.aistones = []
        self.istart = False
        self.board_launched = False
        self.commands = {"START":self.start, "TURN":self.turn, "BEGIN":self.begin, "BOARD":self.board, "INFO":self.info, "END":self.end, "ABOUT":self.about, "DISP":self.disp, "AIDISP": self.aidisp}
        self.ai = ai._ai()
        # for pattern in self.ai.warnpatterns:
        #     print (pattern, len(pattern))

    def run(self):
        while (True):
            try:
                cmd = input()
            except EOFError:
                continue
            self.exec(cmd)

    def exec(self, cmd):
        args = cmd.replace(',', ' ').split()
        if len(args) == 0:
            return
        if self.board_launched:
            if args[0] == "DONE":
                self.done(args[1:])
            else:
                self.load_board_emplacements(args)
            return
        try:
            self.commands[args[0]](args[1:])
        except KeyError:
            print("UNKNOWN unknown command %s" % args[0])

    def create_board(self, size):
        self.goban = [['0' for _ in range(size)] for _ in range(size)]

    def disp(self, args):
        if not self.istart:
            print("ERROR game haven't started")
            return
        for line in self.goban:
            for col in line:
                print(col, end="")
            print("")

    def aidisp(self, args):
        if not self.istart:
            print("ERROR game haven't started")
            return
        self.ai.display_board(self.goban)

    def start(self, args):
        if self.istart:
            print("ERROR START the game have already started")
        if len(args) != 1:
            print("ERROR START expecting 1 argment, given %d" % len(args))
            return
        else:
            try:
                board_size = int(args[0])
            except ValueError:
                print("ERROR START the size must be an integer")
                return
        if board_size != 19 and board_size != 20:
            print("ERROR %d size is not supported" % board_size)
            return
        self.create_board(board_size)
        self.istart = True
        print("OK")

    def turn(self, args):
        if not self.istart:
            print("ERROR game haven't started")
            return
        if len(args) != 2:
            print("ERROR TURN expecting 3 argment, given %d" % len(args))
            return
        else:
            try:
                x , y = int(args[0]), int(args[1])
            except ValueError:
                print("ERROR TURN coordinates must be positive numbers")
                return
        if x < 0 or y < 0:
            print("ERROR TURN coordinates must be positive numbers")
            return
        if x >= len(self.goban) or y >= len(self.goban):
            print("ERROR TURN invalid position")
            return
        self.emplace_stone(x, y, 2)
        self.pstones.append((x,y))
        resx,resy = self.ai.compute(self.goban, self.pstones, self.aistones)
        #resx = random.randint(0, len(self.goban))
        #resy = random.randint(0, len(self.goban))
        print("%d,%d" % (resx, resy))
        self.emplace_stone(resx, resy, 1)
        self.aistones.append((resx, resy))

    def begin(self, args):
        if not self.istart:
            print("ERROR game haven't started")
            return
        if len(args) != 0:
            print("ERROR BEGIN no argument needed")
            return
        resx,resy = self.ai.compute(self.goban, self.pstones, self.aistones)
        #resx = random.randint(0, len(self.goban))
        #resy = random.randint(0, len(self.goban))
        print("%d,%d" % (resx, resy))
        self.emplace_stone(resx, resy, 1)
        self.aistones.append((resx, resy))

    def board(self, args):
        if not self.istart:
            print("ERROR game haven't started")
            return
        if len(args) != 0:
            print("ERROR BOARD no argument needed")
            return
        self.board_launched = True

    def done(self, args):
        if not self.board_launched:
            print("UNKNOWN unknown command DONE")
        if len(args) != 0:
            print("ERROR DONE no argument needed")
            return
        self.board_launched = False
        resx,resy = self.ai.compute(self.goban, self.pstones, self.aistones)
        #resx = random.randint(0, len(self.goban))
        #resy = random.randint(0, len(self.goban))
        print("%d,%d" % (resx, resy))
        self.emplace_stone(resx, resy, 1)
        self.aistones.append((resx, resy))

    def load_board_emplacements(self, args):
        if len(args) != 3:
            print("ERROR BOARD bad emplacement format")
            return
        try:
            x, y, field = int(args[0]), int(args[1]), int(args[2])
        except ValueError:
            print("ERROR BOARD coordinates must be positive numbers and field between 2 and 3")
        if x < 0 or y < 0 or (field != 1 and field != 2):
            print("ERROR BOARD coordinates must be positive numbers and field between 2 and 3")
            return
        if x >= len(self.goban) or y >= len(self.goban):
            print("ERROR BOARD invalid position")
        self.emplace_stone(x, y, field)
        if field == 2:
            self.pstones.append((x,y))
        else:
            self.aistones.append((x, y))

    def emplace_stone(self, x, y, field):
        avatar = 'x' if field == 1 else 'o'
        if self.goban[y][x] != '0':
            print("ERROR BOARD position already occuped")
            return
        self.goban[y][x] = avatar

    def info(self, args):
        pass

    def end(self, args):
        exit (0)

    def about(self, args):
        if len(args) != 0:
            print("ERROR ABOUT no argument needed")
            return
        print("name=\"GomuGomuBrain\", version=\"0.0\", authors=\"Lordnel, Dydywesh, Marso\", country=\"BJ\"")

gomoku = game()
gomoku.run()