import random
import numpy as np
from Characters.Basic_Actions import *

#The spellbook! 
def Create_Spellbook():
    
    #Light spell
    
    def Clearwater_Mirror(Player,Game):
        Player.buffs[0] += 1

    def Arcane_Shield(Player,Game):
        Player.buffs[1] += 1
    
    def Elemental_Mastery(Player,Game):
        Player.buffs[2] +=1

    def Blessing_of_the_Otters(Player, Game): #Otter of greed allows me to draw 2 cards from my deck, greed is good
        if len(Game.spell_deck)>=2: #https://www.youtube.com/watch?v=wuH84iNLJ8U
            Draw(2, Player.hand, Game.spell_deck)
        else:
            Game.spell_deck+=Game.discard_pile
            random.shuffle(Game.spell_deck)
            Game.discard_pile = []
            Draw(2, Player.hand, Game.spell_deck)

    def Fresh_Start(Player, Game):
        while Player.hand:  # More efficient way to clear the hand and draw 4 new cards
            Player.Remove_spell(Player.hand[0].name, Game)
        Draw(4, Player.hand, Game.spell_deck)

    def Time_Warp(Player, Game): #Retrieves a random card
        if Game.discard_pile:
            Card = np.random.choice(Game.discard_pile)
            print(Player.char.name+" picked up "+Card.name)
            Player.hand.append(Card)
            Game.discard_pile.remove(Card)

    def Task_Scramble(Player, Game):
        Game.task_deck += Game.task_board
        Game.task_board.clear()  # Using clear() method to empty the list
        np.random.shuffle(Game.task_deck)
        Draw(9, Game.task_board, Game.task_deck)
    
    #Dark spells
    
    def Elemental_Lock(Player,Game):
        Element = np.random.choice(["Fire","Earth","Air","Water"])
        print("   ",Element)
        for player in Game.players:
            if player.buffs[1]>0:
                player.buffs[1] -= 1
                print("ARCANE PROTECTS "+player.char.name+" FROM YOUR ELEMENTAL LOCK")
            else:
                player.banned_elements.append(Element)
    
    def Chaotic_Swap(Player,Game):
        Target = Choose_enemy(Player,Game)
        if Target.buffs[1]>0:
            Target.buffs[1] -= 1
            print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR CHAOTIC SWAP")
        elif len(Player.hand)>3:
            print(Player.char.name+" swapped hands with "+Target.char.name)
            Player.Remove_spell("Chaotic Swap",Game)
            Target.hand, Player.hand = Player.hand, Target.hand
        else:
            print(Player.char.name+" wasted chaotic swap!")
    
    def Curse_of_the_Otters(Player,Game):
        Target = Choose_enemy(Player,Game)
        if Target.buffs[1]>0:
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
        if Target.buffs[1]>0:
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
            if Target.buffs[1]>0:
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
        if Target.buffs[1]>0:
                Target.buffs[1] -= 1
                print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR DARK THEFT")
        elif len(Target.hand)>0:
            np.random.shuffle(Target.hand)
            print(Target.hand[0].name+" has been YOINKED from"+Target.char.name)
            Player.hand.append(Target.hand[0])
            Target.hand.remove(Target.hand[0])
        else:
            print("Wasted Night Tide!")
    
    def Shadow_Snare(Player,Game):
        Target = Choose_enemy(Player,Game)
        if Target.buffs[1]>0:
                Target.buffs[1] -= 1
                print("ARCANE PROTECTS "+Target.char.name+" FROM YOUR GROTESQUE SNARE")
        else:
            Target.buffs[3] = 2
        print(Target.char.name+" has been cursed to only 2 actions!")

    # Return a dictionary mapping spell names to their corresponding functions
    return {
        "Clearwater Mirror": Clearwater_Mirror,
        "Elemental Mastery": Elemental_Mastery,
        "Arcane Shield": Arcane_Shield,
        "Blessing of the Otters": Blessing_of_the_Otters,
        "Fresh Start": Fresh_Start,
        "Time Warp": Time_Warp,
        
        "Task Scramble": Task_Scramble,
        "Chaotic Swap":Chaotic_Swap,
        "Elemental Lock":Elemental_Lock,
        "Curse of the Otters":Curse_of_the_Otters,
        "Phantom Paw":Phantom_Paw,
        "Spectral Siphon":Spectral_Siphon,
        "Night Tide Theft":Night_Tide_Theft,
        "Shadow Snare":Shadow_Snare
    }

Spellbook = Create_Spellbook()  #Maybe this should be part of a class idk