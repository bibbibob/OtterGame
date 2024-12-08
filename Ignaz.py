# cards.py
from Characters.Basic_Spellbook import Spellbook
from Characters.Basic_Actions import *


# Define Character Cards
class CharacterCard:
    def __init__(self, name,Spellbook = Spellbook,):
        self.name = name
        self.Spellbook = Spellbook.copy()
    def Pregame(self,Player,Game):
        pass
    def Endgame(self,Player,Game):
        pass
    def Attempt_Solve(self,Task,Player,Game): #Just a regular attempt at solving tasks
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
                    if Task.solving_type_1=="Fire" or Task.solving_type_2=="Fire":
                        Player.buffs[4] = 1
        elif Task.points == 1:
            if (Task.solving_spell_1 in HAND) and (Task.solving_type_1 not in Player.banned_elements):
                print(Player.char.name+" solved: "+str(Task.name))
                Player.Remove_spell(Task.solving_spell_1,Game)
                Player.solved_tasks.append(Task)
                Player.points += 1
                Game.task_board.remove(Task)
                if Task.solving_type_1=="Fire":
                        Player.buffs[4] = 1
            elif (Task.solving_spell_2 in HAND) and (Task.solving_type_2 not in Player.banned_elements):
                print(Player.char.name+" solved: "+str(Task.name))
                Player.Remove_spell(Task.solving_spell_2,Game)
                Player.solved_tasks.append(Task)
                Player.points += 1
                Game.task_board.remove(Task)
                if Task.solving_type_2=="Fire":
                        Player.buffs[4] = 1
            
    def Attempt_Solve_Buffed(self,Task,Player,Game): #Attempting to solve tasks with elemental mastery buff active
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
                if Task.solving_type_1=="Fire" or Task.solving_type_2=="Fire":
                        Player.buffs[4] = 1
                return -1 #If successful remove an elemental mastery point
        return 0
    
    def Main(self,Player,Game):
        #Main Phase
        print(Player.banned_elements," are banned elements this turn")
        Finish = 0
        Player.buffs[4] = 1
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
                    Player.char.Attempt_Solve(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []

            for i,task in enumerate(Game.task_board): #Attempts to solve 3p using the buffed mode from "Elemental Mastery"
                if task.points == 3 and sum(Player.buffs[2:4])>=2: 
                    Player.buffs[2] += Player.char.Attempt_Solve_Buffed(task,Player,Game)
                    if Max_Actions(Player,Game):
                        return []

            for i,task in enumerate(Game.task_board):
                if task.points == 1: #Then attempts to solve 1 point tasks
                    Player.char.Attempt_Solve(task,Player,Game)
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
        if Player.buffs[4] == 1:
            Target = Choose_enemy(Player,Game)
            for card in Target.solved_tasks.copy():
                if card.points == 1:
                    Game.task_deck.append(card)
                    Target.solved_tasks.remove(card)
                    Target.points -= 1
                    np.random.shuffle(Game.task_deck)
                    break
        Player.buffs[4] = 0
        
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
Ignaz = CharacterCard("Ignaz")