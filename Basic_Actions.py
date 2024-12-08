#Actions
import random
import numpy as np
import copy

class Player:
    def __init__(self):
        self.char = 0
        self.hand = []
        self.points = 0
        self.solved_tasks = []
        self.buffs= [0,0,0,999,0] #0 is Mirror, #1 is Arcane Shield, #2 is Elemental mastery #3 is Shadow Snare #4 is 
                                  # A character specific buff that vary. Often a "once a game" ability.
        self.banned_elements = [] 
    def Remove_spell(self,Spell_name,Game):
        self.buffs[3] -= 1
        try:
            HAND = [x.name for x in self.hand]
            i = HAND.index(Spell_name)
            if self.buffs[0]>0 and (self.hand[i].card_type not in ["Light","Dark"]):
                self.buffs[0] += -1
                print("Discarding of "+self.hand[i].name+" blocked due to Clearwater Mirror!")
            else:
                Game.discard_pile.append(self.hand[i])
                print("     ",self.hand[i].name," is being been discarded")
                self.hand.remove(self.hand[i])
        except:
            print("Failed discard") #This should happen if elemental mastery allowed a task to complete with a card not in hand
class Gamestate:
    def __init__(self,spell_deck,task_deck,task_board,discard_pile,players):
        self.spell_deck = spell_deck
        self.task_deck = task_deck
        self.task_board = task_board
        self.discard_pile = discard_pile
        self.players = players
        self.end_game = False

def Choose_enemy(Player,Game): #Picks random enemy
    Enemy = Game.players.copy()
    Enemy.remove(Player)
    return np.random.choice(Enemy)

def Max_Actions(Player,Game):
    return Player.buffs[3] == 0

def Shuffle(Deck): #Returns a copy of a shuffled deck. (Just to initialize a game)
    A = copy.deepcopy(Deck)
    np.random.shuffle(A)
    return A

def Draw(i,Object,Deck): #Draws i cards from a deck and adds them to the object (Hand or board)
    #Returns first cards drawn, and then the state of the deck.
    Object += Deck[0:i]
    del Deck[0:i]
    
def Attempt_Solve(Task,Player,Game): #Just a regular attempt at solving tasks
    HAND = [x.name for x in Player.hand]
    if Task.points == 3:
        if Task.solving_spell_1 in HAND and Task.solving_spell_2 in HAND:
            if (Task.solving_type_1 not in Player.banned_elements) and (Task.solving_type_2 not in Player.banned_elements):
                print(Player.char.name+" solved: "+str(Task.name))
                Player.Remove_spell(Task.solving_spell_1,Game)
                Player.Remove_spell(Task.solving_spell_2,Game)
                Player.solved_tasks.append(Task)
                Player.points += 3
                Game.task_board.remove(Task)
    elif Task.points == 1:
        if (Task.solving_spell_1 in HAND) and (Task.solving_type_1 not in Player.banned_elements):
            print(Player.char.name+" solved: "+str(Task.name))
            Player.Remove_spell(Task.solving_spell_1,Game)
            Player.solved_tasks.append(Task)
            Player.points += 1
            Game.task_board.remove(Task)
        elif (Task.solving_spell_2 in HAND) and (Task.solving_type_2 not in Player.banned_elements):
            print(Player.char.name+" solved: "+str(Task.name))
            Player.Remove_spell(Task.solving_spell_2,Game)
            Player.solved_tasks.append(Task)
            Player.points += 1
            Game.task_board.remove(Task)
            
def Attempt_Solve_Buffed(Task,Player,Game): #Attempting to solve tasks with elemental mastery buff active
    HAND = [x.name for x in Player.hand]
    if Task.points == 3 and Player.buffs[2]>0:
        if ((Task.solving_spell_1 in HAND) and (Task.solving_type_1 not in Player.banned_elements)) \
        or ((Task.solving_spell_2 in HAND) and (Task.solving_type_2 not in Player.banned_elements)):
            print(Player.char.name+" solved: "+str(Task.name)+" using buff superiority from EM")
            Player.Remove_spell(Task.solving_spell_1,Game)
            Player.Remove_spell(Task.solving_spell_2,Game) #There is a fail case if spell isn't in hand, which one should not be.
            Player.solved_tasks.append(Task)
            Player.points += 3
            Game.task_board.remove(Task)
            return -1 #If successful remove an elemental mastery point
    return 0