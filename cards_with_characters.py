# cards.py

# Define Character Cards
class CharacterCard:
    def __init__(self, name):
        self.name = name

# Define Spell Cards
class SpellCard:
    def __init__(self, name, card_type, timing=0 ,copies=2):
        self.name = name
        self.card_type = card_type
        self.copies = copies
        self.timing = timing

# Define Task Cards
class TaskCard:
    def __init__(self, name, points, solving_spell_1, solving_spell_2, solving_type_1, solving_type_2):
        self.name = name
        self.points = points
        self.solving_spell_1 = solving_spell_1
        self.solving_type_1 = solving_type_1
        self.solving_spell_2 = solving_spell_2
        self.solving_type_2 = solving_type_2

# Define Item Cards
class ItemCard:
    def __init__(self, name):
        self.name = name

# Initialize Character Cards
character_names = ["April", "Artemis", "Beirui", "Blaze", "Claude", "Crust", "Eclipse", "Eira", "Feng", "Franzi", "Frost", "Hsu", "Ignaz", "Ivy", "Izokuma", "Jin", "Jules", "Kaze", "Kuro", "Luna", "Martin", "Maufi", "Nori", "Petal", "Prisma", "Rokan", "Shiro", "Yura", "Tim", "Daiko"]

#Initialize Character Cards
import importlib

#character_names = ["April", "Artemis", "Beirui", "Blaze", "Claude", "Crust", "Eclipse", "Eira", "Feng", "Franzi", "Frost", "Hsu", "Ignaz", "Ivy", "Izokuma", "Jin", "Jules", "Kaze", "Kuro", "Luna", "Martin", "Maufi", "Nori", "Petal", "Prisma", "Rokan", "Shiro", "Yura", "Tim", "Daiko"]
character_names = ["Dude","April","Artemis","Beirui","Blaze","Claude","Crust","Eclipse","Eira","Feng","Franzi","Frost","Hsu","Ignaz","Izokuma","Jin","Jules","Kaze","Kuro","Luna","Martin","Maufi","Nori","Rokan","Petal","Prisma","Shiro","Yura","Daiko"]
#Missing: Ivy,  Petal, Tim
character_cards = []

for name in character_names:
    # Dynamically import the module corresponding to each character's name
    module = importlib.import_module(f"Characters.{name}")
    
    # Assume the variable you want to import is named identically to the character, for simplicity
    # Adjust this as necessary if the variable has a different naming scheme
    character_card = getattr(module, name)
    
    character_cards.append(character_card)

# Now character_cards will contain the imported variables from each character's module


# Initialize Spell Cards (with special handling for Arcane Shield's 4 copies)
spell_cards_data = [
    #Light
    ("Clearwater Mirror", "Light",2, 1), 
    ("Blessing of the Otters", "Light",2, 1), 
    ("Elemental Mastery", "Light",2, 1),
    ("Fresh Start", "Light",2, 2), 
    ("Arcane Shield", "Light", 4, 1), 
    ("Time Warp", "Light",2, 1), 
    ("Task Scramble", "Light",2, 2),
    #Dark
    ("Elemental Lock", "Dark",2, 2), 
    ("Chaotic Swap", "Dark",10, 2), 
    ("Curse of the Otters", "Dark",2, 1),
    ("Phantom Paw", "Dark",2, 1), 
    ("Spectral Siphon", "Dark",2, 1), 
    ("Night Tide Theft", "Dark",2, 1), 
    ("Shadow Snare", "Dark",2, 1),
    # Elemental Spells
    ("Tidal Tsunami", "Water", 5 ,0), 
    ("Glacial Frenzy", "Water", 5 ,0), 
    ("Flow Focus", "Water", 5 ,0),
    ("Metal Momentum", "Earth", 5 ,0), 
    ("Terraclean", "Earth", 5 ,0), 
    ("Blossom Bloom", "Earth", 5, 0),
    ("Hurricane Hustle", "Air", 5, 0), 
    ("Zephyr Zip", "Air", 5, 0), 
    ("Whirlwind Whisk", "Air", 5, 0),
    ("Thermal Burst", "Fire", 5, 0), 
    ("Inferno Infusion", "Fire", 5, 0), 
    ("Solar Flare", "Fire", 5, 0)
]
spell_cards = [SpellCard(name, card_type, timing) for name, card_type, copies, timing in spell_cards_data for _ in range(copies)]
#print(f"Total Spell Cards: {len(spell_cards)}")

# Initialize Item Cards
item_names = [
  "Bursting Acorn", 
  "Coral Crown", 
  "Darkened Kelp Knot", 
  "Ebb and Flow", 
  "Echoing Whiskers", 
  "Elder Otter's Talisman", 
  "Elemental Lock +", 
  "Firefish Fin", 
  "Focus Lens", 
  "Foreseeing Frog Eye", 
  "Gourmet", 
  "Green Paw", 
  "Heart-shaped Pebble", 
  "Nightfish Grasp", 
  "Otter's Diving Goggles", 
  "Overflow Staff", 
  "Pearl of Prosperity", 
  "Predator's Claw", 
  "Rainbow Scale", 
  "Ripple Rune", 
  "Shoreline Sapphire", 
  "Sibling Locket", 
  "Sparkling Dewdrop", 
  "Spavellous Fur", 
  "Starlight Shell", 
  "Sunbeam Talisman", 
  "Swamp Fish Snare", 
  "Time-Twisted Seaweed", 
  "Wind Dancer's Feather", 
  "Wise Clamshell"]

item_cards = [ItemCard(name) for name in item_names]

# Initialize Updated Task Cards
task_cards_data = [
    ("Making Tea", 1, "Tidal Tsunami", "Thermal Burst", "Water", "Fire"),
    ("Doing Laundry", 3, "Tidal Tsunami", "Solar Flare", "Water", "Fire"),
    ("Watering Plants", 3, "Flow Focus", "Blossom Bloom", "Water", "Earth"),
    ("Making Ice-Matcha Latte", 1, "Glacial Frenzy", "Thermal Burst", "Water", "Fire"),
    ("Taking a Shower", 1, "Glacial Frenzy", "Inferno Infusion", "Water", "Fire"),
    ("Doing the Dishes", 1, "Glacial Frenzy", "Whirlwind Whisk", "Water", "Air"),
    ("Fixing leaking faucet", 1, "Flow Focus", "Metal Momentum", "Water", "Earth"),
    ("Flossing teeth", 1, "Flow Focus", "Zephyr Zip", "Water", "Air"),
    ("Taking out the trash", 1, "Tidal Tsunami", "Hurricane Hustle", "Water", "Air"),
    ("Making Bento", 3, "Thermal Burst", "Whirlwind Whisk", "Fire", "Air"),
    ("Growing Vegetables", 1, "Solar Flare", "Blossom Bloom", "Fire", "Earth"),
    ("Paying Bills", 1, "Solar Flare", "Whirlwind Whisk", "Fire", "Air"),
    ("Ironing Clothes", 1, "Inferno Infusion", "Metal Momentum", "Fire", "Earth"),
    ("Taking Hot Stone Spa", 1, "Inferno Infusion", "Terraclean", "Fire", "Earth"),
    ("Raking Leaves", 1, "Blossom Bloom", "Hurricane Hustle", "Earth", "Air"),
    ("Returning Pfand Bottles", 3, "Metal Momentum", "Zephyr Zip", "Earth", "Air"),
    ("Vacuuming the floor", 1, "Terraclean", "Zephyr Zip", "Earth", "Air"),
    ("Dusting the attic", 1, "Terraclean", "Hurricane Hustle", "Earth", "Air")
]


# Use a list comprehension with a nested loop to create three copies of each task card
task_cards = [TaskCard(name, points, solving_spell_1, solving_spell_2, solving_type_1, solving_type_2) for name, points, solving_spell_1, solving_spell_2, solving_type_1, solving_type_2 in task_cards_data for _ in range(3)]