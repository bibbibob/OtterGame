# cards.py
from Characters.Basic_Spellbook import Spellbook
from Characters.Basic_Actions import *


# Define Character Cards
class CharacterCard:
    def __init__(self, name,Spellbook = Spellbook,):
        self.name = name
        self.Spellbook = Spellbook.copy()
    def Attempt_Solve_Ability_1(self,Task,Player,Game):
        HAND = [x.name for x in Player.hand]
        if "Earth" not in Player.banned_elements and Task.points == 1 and Player.buffs[4] > 0:
            P = Player.points
            if Task.solving_type_1 == "Water" and ("Metal Momentum" in HAND):
                print(Player.char.name + " solved: " + str(Task.name))
                Player.Remove_spell("Metal Momentum", Game)
                Player.solved_tasks.append(Task)
                Player.points += 1
            if Task.solving_type_1 == "Water" and ("Blossom Bloom" in HAND):
                print(Player.char.name + " solved: " + str(Task.name))
                Player.Remove_spell("Blossom Bloom", Game)
                Player.solved_tasks.append(Task)
                Player.points += 1
            if Task.solving_type_1 == "Water" and ("Terraclean" in HAND):
                print(Player.char.name + " solved: " + str(Task.name))
                Player.Remove_spell("Terraclean", Game)
                Player.solved_tasks.append(Task)
                Player.points += 1
            if Player.points > P:
                Player.buffs[4] = 0
                print("Eira used her ability to transform earth to water!")
                
    def Attempt_Solve_Ability_3(self,Task, Player, Game):  # Attempting to solve tasks with elemental mastery buff active
        HAND = [x.name for x in Player.hand]
        if Task.points == 3 and Player.buffs[4] > 0:
            P = Player.points
            if Task.solving_type_1 == "Water": #This abuses that for some reason every task with Water is in solve_1
                if ("Blossom Bloom" in HAND) and (Task.solving_spell_2 in HAND) and (Task.name != "Watering Plants" or HAND.count("Blossom Bloom") >= 2):
                    print(Player.char.name + " solved: " + str(Task.name))
                    Player.Remove_spell("Blossom Bloom", Game)
                    Player.Remove_spell(Task.solving_spell_2, Game)
                    Player.solved_tasks.append(Task)
                    Player.points += 3
                    Game.task_board.remove(Task)
                elif ("Metal Momentum" in HAND) and (Task.solving_spell_2 in HAND):
                    print(Player.char.name + " solved: " + str(Task.name))
                    Player.Remove_spell("Metal Momentum", Game)
                    Player.Remove_spell(Task.solving_spell_2, Game)
                    Player.solved_tasks.append(Task)
                    Player.points += 3
                    Game.task_board.remove(Task)
                elif ("Terraclean" in HAND) and (Task.solving_spell_2 in HAND):
                    print(Player.char.name + " solved: " + str(Task.name))
                    Player.Remove_spell("Terraclean", Game)
                    Player.Remove_spell(Task.solving_spell_2, Game)
                    Player.solved_tasks.append(Task)
                    Player.points += 3
                    Game.task_board.remove(Task)
            if Player.points > P:
                Player.buffs[4] = 0
                print("Eira used her ability to transform earth to water!")
    def Pregame(self,Player,Game):
        pass
    def Main(self,Player,Game):
        #Main Phase
        print(Player.banned_elements," are banned elements this turn")
        Player.buffs[4] = 1
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
                if task.points == 3 and Player.buffs[3]>=2: #Attempts to solve 3 points tasks with ability
                    self.Attempt_Solve_Ability_3(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []
            
            for i,task in enumerate(Game.task_board):
                if task.points == 1: #Then attempts to solve 1 point tasks
                    Attempt_Solve(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []
                    
            for i,task in enumerate(Game.task_board):
                if task.points == 1: #Then attempts to solve 1 point tasks with ability
                    self.Attempt_Solve_Ability_1(task,Player,Game)
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
Eira = CharacterCard("Eira")