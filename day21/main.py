from collections import defaultdict, namedtuple
import sys
import os
from typing import DefaultDict, NamedTuple 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataclasses import dataclass

from utils.read_file import read_file
import numpy as np
import random 
import itertools
import copy
def parse_input(input_list):
    startpos1 = int(input_list[0][-1])
    startpos2 = int(input_list[1][-1])

    return startpos1, startpos2

class Player:
    def __init__(self, id: int, position: int, score:int = 0, win_count = 1000):
        self.internal_position = position - 1 # [0-9] to allow for modulo
        self.score = score
        self.ID = id
        self.win_score = win_count

    def update(self, steps):
        self.internal_position = (self.internal_position + steps) % 10
        self.score += self.get_position()

    def get_position(self):
        return self.internal_position + 1
    
    def has_won(self) -> bool:
        return self.score >= self.win_score

    def __repr__(self):
        return f"Player{self.ID}: pos = {self.get_position()}, score = {self.score}"

class BaseDice:
    def __init__(self) -> None:
        self.count  = 0
    def roll(self) -> int:
        self.count += 1
        

class DeterministicDice(BaseDice):
    def __init__(self, max_state= 100) -> None:
        super().__init__()
        self.state  = 0
        self.max_state = max_state

    def roll(self):
        super().roll()
        self.state += 1
        if self.state > self.max_state:
            self.state = 1

        return self.state
        

class Game:
    def __init__(self,pos1:int, pos2: int, dice: BaseDice, win_count):
        self.turn = 0
        self.players = [Player(0,pos1, win_count= win_count), Player(1,pos2, win_count= win_count)]
        self.dice = dice

    def do_turn(self, values  =None) -> bool:
        if not values:
            values = [self.dice.roll() for _ in range(3)]
        step = sum(values)
        self.players[self.turn].update(step)

        return self.players[self.turn].has_won()
    
    def play_game(self):
        while True:
            has_won = self.do_turn()
            if has_won:
                return self.players
            else:
                self.turn = 1 - self.turn


class DiracGames:
    def __init__(self, pos1: int, pos2: int, dice_n_sideds: int):
        self.games = [Game(pos1,pos2, None, 21)]
        self.win_count = [0,0]
    
    def play(self):
        i= 0
        while (len(self.games) > 0):
            i += 1
            game = self.games.pop(0)
            for values in itertools.product([1,2,3],repeat = 3):
                g = copy.deepcopy(game)
                has_won = g.do_turn(values)
                if has_won:
                    self.win_count[game.turn] += 1
                    print(self.win_count)

                else: 
                    g.turn = 1 - g.turn
                    self.games.append(g)
            if i % 1000 ==0 :
                print(self.win_count)
        return self.win_count


### other approach...

# what makes a game state -> 
# pos1, pos2, score1, score2 -> 10*10*21*21 different games = 45K
# at each step the scores go at least + 3 -> game over in < 20 steps
# so O(9 000 000)

# old approach: branch factor = 27 -> 27**20 = O(infinity)
GameState = namedtuple("GameState"," p1 p2 score1 score2")

def fast_part2(p1,p2):

    game_scores = defaultdict(lambda: 0)
    game_scores[GameState(p1,p2,0,0)] = 1

    win_count  = [0,0]
    turn = 0

    for _ in range(20):
        new_game_scores = defaultdict(lambda: 0)
        for p1 in range(1,11):
            for p2 in range(1,11):
                for score1 in range(21):
                    for score2 in range(21):
                        if game_scores[GameState(p1,p2,score1,score2)] == 0:
                            continue
                        for values in itertools.product([1,2,3],repeat = 3):
                            value = sum(values)
                            if turn == 0:
                                p1_n, p2_n = (p1 + value) if p1+ value <= 10 else p1 + value - 10, p2
                                new_score1, new_score2  = score1 + p1_n, score2
                    
                            else: 
                                p1_n, p2_n = p1, p2 + value if p2+ value <= 10 else p2 + value -10 
                                new_score1, new_score2 = score1, score2  +p2_n

                            if max(new_score2, new_score1) >= 21:
                                win_count[turn] += game_scores[GameState(p1,p2,score1,score2)]
                            else:
                                count = game_scores[GameState(p1,p2,score1,score2)]
                                new_game_scores[GameState(p1_n,p2_n,new_score1,new_score2)] += count

        game_scores = new_game_scores
        turn  = 1 - turn
        print(win_count)
    print(max(win_count))

    



def get_part1_score(p1: Player, p2: Player, dice: DeterministicDice):
    if p1.has_won():
        return p2.score * dice.count
    else:
        return p1.score * dice.count


def part1(input_list):
    pos1, pos2 = parse_input(input_list)
    dice = DeterministicDice()
    game = Game(pos1,pos2,dice)

    p1, p2 = game.play_game()

    print(get_part1_score(p1,p2,dice))
    
def part2(input_list):
    pos1, pos2 = parse_input(input_list)
    game = DiracGames(pos1,pos2,3)
    print(game.play())


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))

    #print(parse_input(test_list))
    #part1(input_list)
    #part1(input_list)
    #part2(input_list)
    fast_part2(3,10)
