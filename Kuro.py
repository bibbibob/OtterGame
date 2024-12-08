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
            if Finish==1 and Player.buffs[4]==1:
                if len(Player.hand)>1:
                    print("Kuro used ability!")
                    print("Cards in hand; ",[Card.name for Card in Player.hand])
                    np.random.shuffle(Game.discard_pile)
                    for Card in Game.discard_pile:
                        if Card.card_type == "Dark":
                            print(f"Kuro swapped two cards for {Card.name}")
                            Player.hand.append(Card)
                            Game.discard_pile.remove(Card)
                            Draw(2,Game.discard_pile,Player.hand)
                            for card in Game.discard_pile[-2:]:
                                print(f"The card swapped was {card.name}")
                            Finish = 0
                            Player.buffs[4] = 0
                            print("Cards in hand; ",[Card.name for Card in Player.hand])
                            break
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
Kuro = CharacterCard("Kuro")