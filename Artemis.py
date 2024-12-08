# cards.py
from Characters.Basic_Spellbook import Spellbook
from Characters.Basic_Actions import *

Spellbook = Spellbook.copy()
#Custom Spells

def Elemental_Lock(Player,Game):
    Element = np.random.choice(["Fire","Earth","Air","Water"])
    print("   ",Element)
    for player in Game.players:
        if False:
            player.buffs[1] -= 1
            print("ARCANE PROTECTS "+player.char.name+" FROM YOUR ELEMENTAL LOCK")
        else:
            player.banned_elements.append(Element)
            
def Chaotic_Swap(Player,Game):
    Target = Choose_enemy(Player,Game)
    if len(Player.hand)>3:
        print(Player.char.name+" swapped hands with "+Target.char.name)
        Player.Remove_spell("Chaotic Swap",Game)
        Target.hand, Player.hand = Player.hand, Target.hand
    else:
        print(Player.char.name+" wasted chaotic swap!")

def Curse_of_the_Otters(Player,Game):
    print("DIE INSECTS")
    Target = Choose_enemy(Player,Game)
    if False: #Artemis can't be blocked by buffs
        Target.buffs[1] -= 1
        print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR NASTY CURSE")
    else:
        for k in range(2):
            if len(Target.hand)>0:
                Game.discard_pile.append(Target.hand[0])
                print(Target.char.name+" discarded ",Target.hand[0].name)
                Target.hand.remove(Target.hand[0])
            else:
                print(Target.char.name+" is empty handed")

def Phantom_Paw(Player,Game):
    Target = Choose_enemy(Player,Game)
    Sorted_Tasklist = sorted(Target.solved_tasks, key=lambda x: x.points, reverse=True)
    if False:
        Target.buffs[1] -= 1
        print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR FILTHY PAWS")
    elif len(Sorted_Tasklist)>0:
        Task = Sorted_Tasklist[0] 
        Player.solved_tasks.append(Task)
        Player.points += Task.points
        Target.points -= Task.points
        Target.solved_tasks.remove(Task)
        print(Task.name+" has been stolen from "+Target.char.name+"!")
    else:
        print(Player.char.name+" pawed nothing!")

def Spectral_Siphon(Player,Game):
    Enemies = Game.players.copy()
    Enemies.remove(Player)
    Element = np.random.choice(["Fire","Earth","Air","Water"])
    print("    Naming: ",Element)
    for Target in Enemies:
        if False:
            Target.buffs[1] -= 1
            print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR VILE SIPHON")
        else:
            for Card in Target.hand.copy():
                if Card.card_type == Element:
                    Player.hand.append(Card)
                    Target.hand.remove(Card)
                    print(Card.name+" has been YOINKED from "+Target.char.name)

def Night_Tide_Theft(Player,Game):
    Target = Choose_enemy(Player,Game)
    if False:
            Target.buffs[1] -= 1
            print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR VILE SIPHON")
    elif len(Target.hand)>0:
        np.random.shuffle(Target.hand)
        print(Target.hand[0].name+" has been YOINKED from"+Target.char.name)
        Player.hand.append(Target.hand[0])
        Target.hand.remove(Target.hand[0])
    else:
        print(Player.char.name+" wasted Night Tide!")

Spellbook["Elemental Lock"] = Elemental_Lock
Spellbook["Chaotic Swap"] = Chaotic_Swap
Spellbook["Curse of the Otters"] = Curse_of_the_Otters
Spellbook["Night Tide Theft"] =  Night_Tide_Theft
Spellbook["Spectral Siphon"] = Spectral_Siphon
Spellbook["Phantom Paw"] = Phantom_Paw
Spellbook["afafa"] = Phantom_Paw
# Define Character Cards
class CharacterCard:
    def __init__(self, name,Spellbook = Spellbook,):
        self.name = name
        self.Spellbook = Spellbook
    def Pregame(self,Player,Game):
        pass
    def Main(self,Player,Game):
        #Main Phase
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
Artemis = CharacterCard("Artemis")