# cards.py
from Characters.Basic_Spellbook import Spellbook
from Characters.Basic_Actions import *

#Defines a custom task card called Frozen
class TaskCard:
    def __init__(self, name, points, solving_spell_1, solving_spell_2, solving_type_1, solving_type_2):
        self.name = name
        self.points = points
        self.solving_spell_1 = solving_spell_1
        self.solving_type_1 = solving_type_1
        self.solving_spell_2 = solving_spell_2
        self.solving_type_2 = solving_type_2

Frozen_spells = 2
# Define Character Cards
class CharacterCard:
    def __init__(self, name,Spellbook = Spellbook,):
        self.name = name
        self.Spellbook = Spellbook.copy()
        self.ability=[TaskCard("Frozen",0,"IMPOSSIBLE","IMPOSSIBLE","ICE","ICE") for i in range(Frozen_spells)]
    def Pregame(self,Player,Game):
        print(TaskCard("Frozen",0,"IMPOSSIBLE","IMPOSSIBLE","ICE","ICE").name)
        Player.buffs[4] = 1
        print("Frost starting ability hand: ",[X.name for X in self.ability])
    def Main(self,Player,Game):
        #Main Phase
        if Player.buffs[4] == 0:
            print("Locating Frozen spells!")
            C=0
            for i,Task in enumerate(Game.task_board):
                if Task.name == "Frozen":
                    print(f"Frost has unfrozen {self.ability[C].name}")
                    self.ability[C],Game.task_board[i] = Game.task_board[i],self.ability[C]
                    C += 1
            for i,Task in enumerate(Game.task_deck):
                if Task.name == "Frozen":
                    print(f"Frost has unfrozen {self.ability[C].name} from the deck")
                    self.ability[C],Game.task_deck[i] = Game.task_deck[i],self.ability[C]
                    C += 1
            print("Frost ability hand: ",[X.name for X in self.ability])
        
        print(Player.banned_elements," are banned elements this turn")
        Finish = 0
        while Finish == 0:

            Finish = 1

            for Spell in Player.hand.copy():
                if (Spell.card_type == "Light" and Spell.timing == 1) or (Spell.card_type == "Dark" and Spell.timing == 1):
                    print(Player.char.name," used ",Spell.name)
                    self.Spellbook[Spell.name](Player,Game)
                    Player.Remove_spell(Spell.name,Game)
                    Finish = 0
                    if Max_Actions(Player,Game):
                        return []

            for i,task in enumerate(Game.task_board):
                if task.points == 3 and Player.buffs[3]>=2: #Attempts to solve 3 points tasks first
                    Attempt_Solve(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []

            for i,task in enumerate(Game.task_board): #Attempts to solve 3p using the buffed mode from "Elemental Mastery"
                if task.points == 3 and sum(Player.buffs[2:4])>=2: 
                    Player.buffs[2] += Attempt_Solve_Buffed(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []

            for i,task in enumerate(Game.task_board):
                if task.points == 1: #Then attempts to solve 1 point tasks
                    Attempt_Solve(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []

            for Spell in Player.hand:
                if (Spell.card_type == "Light" and Spell.timing == 2) or (Spell.card_type == "Dark" and Spell.timing == 2):
                    print(Player.char.name," used the almighty power of ",Spell.name)
                    Finish = 0
                    self.Spellbook[Spell.name](Player,Game)
                    Player.Remove_spell(Spell.name,Game)
                    if Max_Actions(Player,Game):
                        return []
    def Wrap_up(self,Player,Game):
        Player.buffs[4] = 0
        C=0
        for i,Task in enumerate(Game.task_board):
            if Task.points == 3 and C<Frozen_spells:
                self.ability[C],Game.task_board[i] = Game.task_board[i],self.ability[C]
                C += 1
        for i,Task in enumerate(Game.task_board):
            if Task.points == 1 and C<Frozen_spells:
                self.ability[C],Game.task_board[i] = Game.task_board[i],self.ability[C]
                C += 1
        print("Frost has frozen ",[X.name for X in self.ability])
        #Draw Phase
        Player.banned_elements.clear()
        Player.buffs[3] = 999

        if len(Player.hand)<7:
            if len(Game.spell_deck) < 7-len(Player.hand): #Shuffles if deck is too low
                Game.spell_deck+=Game.discard_pile
                random.shuffle(Game.spell_deck)
                Game.discard_pile = []
            Draw(7-len(Player.hand),Player.hand,Game.spell_deck)
        #Refill Phase
        if len(Game.task_board)<9:
            if 9-len(Game.task_board) >= len(Game.task_deck):
                Game.end_game = True
            Draw(min(9-len(Game.task_board),len(Game.task_deck)),Game.task_board,Game.task_deck)
        if Player.points >= 20:
            Game.end_game = True
Frost = CharacterCard("Frost")