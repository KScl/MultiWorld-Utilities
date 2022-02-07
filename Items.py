import logging


def GetBeemizerItem(world, player, item):
    item_name = item if isinstance(item, str) else item.name
    if world.beemizer[player] and item_name in trap_replaceable:
        if world.random.random() < world.beemizer[player] * 0.25:
            if world.random.random() < (0.5 + world.beemizer[player] * 0.1):
                return "Bee Trap" if isinstance(item, str) else ItemFactory("Bee Trap", player)
            else:
                return "Bee" if isinstance(item, str) else ItemFactory("Bee", player)
        else:
            return item
    else:
        return item


def ItemFactory(items, player):
    from BaseClasses import Item
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            ret.append(Item(item, *item_table[item], item_hint_text.get(item), item_credit_text.get(item), player))
        else:
            raise Exception(f"Unknown item {item}")

    if singleton:
        return ret[0]
    return ret

# Items that should change the Pedestal credit text to "sleep again..."
plural_pedestal_credit = [
    'Fighter Sword & Shield', # the sword and shield
    'Bow', # the stick and twine
    'Progressive Bow', # the stick and twine
    'Progressive Bow (Alt)', # the stick and twine
    'Power Glove', # and the grey mittens
    'Flippers', # and the toewebs
    'Mushroom', # and the legal drugs
    'Pegasus Boots', # and the sprint shoes
    'Bombs (3)', # and the explosions
    'Bombs (10)', # and the explosions
    'Bee Trap', # and the sting buddies
]

# Regular, Pedestal, Tablet, Local Pedestal, Local Tablet
item_hint_text = {
    'Nothing':                        ('nothing',                "Surprise! It's literally nothing", None, 'The sword is a lie', None),
    # Swords
    'Fighter Sword & Shield':         ('the Sword and Shield',   "Your uncle's armaments lay here together", None, None, None),
    'Fighter Sword':                  ('the Fighter Sword',      'A pathetic sword rests here!', None, None, None),
    'Master Sword':                   ('the Master Sword',       'I beat barries and pigs alike', None, 'I thought this was meant to be randomized?', 'Look at me! I am the pedestal!'),
    'Tempered Sword':                 ('the Tempered Sword',     "I stole the blacksmith's job!", None, None, None),
    'Golden Sword':                   ('the Golden Sword',       'The butter sword rests here!', None, None, None),
    'Progressive Sword':              ('a Sword',                'A better copy of your sword for your time', None, None, None),
    # Shields
    'Blue Shield':                    ('the Blue Shield',        'Now you can defend against pebbles!', None, None, None),
    'Red Shield':                     ('the Red Shield',         'Now you can defend against fireballs!', None, None, None),
    'Mirror Shield':                  ('the Mirror Shield',      'Now you can defend against lasers!', None, None, None),
    'Progressive Shield':             ('a shield',               'Have a better blocker in front of you', None, None, None),
    # Mail / Armor
    'Blue Mail':                      ('the Blue Mail',          "Now you're a blue elf!", None, None, None),
    'Red Mail':                       ('the Red Mail',           "Now you're a red elf!", None, None, None),
    'Progressive Mail':               ('some armor',             'Time for a change of clothes?', None, None, None),
    # Gloves
    'Power Glove':                    ('the Glove',              'Now you can lift weak stuff!', None, None, None),
    'Titans Mitts':                   ('the Mitts',              'Now you can lift heavy stuff!', None, None, None),
    'Progressive Glove':              ('a glove',                'A way to lift heavier things', None, None, None),
    # Bow
    'Bow':                            ('the Bow',                'You have chosen the archer class.', None, None, None),
    'Progressive Bow':                ('a Bow',                  'You have chosen the archer class.', None, None, None),
    'Progressive Bow (Alt)':          ('a Bow',                  'You have chosen the archer class.', None, None, None),
    'Silver Bow':                     ('the Silver Bow',         'Buy 1 Silver, get Archery for free.', None, None, None),
    'Silver Arrows':                  ('the Silver Arrows',      'Do you fancy silver tipped arrows?', None, None, None),
    # Medallions
    'Bombos':                         ('Bombos',                 'Burn, baby, burn! Fear my ring of fire!', None, None, None),
    'Ether':                          ('Ether',                  'This magic coin freezes everything!', None, None, None),
    'Quake':                          ('Quake',                  'Maxing out the Richter scale is what I do!', None, None, None),
    # Boomerangs
    'Blue Boomerang':                 ('the Blue Boomerang',     'No matter what you do, blue returns to you', None, None, None),
    'Red Boomerang':                  ('the Red Boomerang',      'No matter what you do, red returns to you', None, None, None),
    # Flutes
    'Flute':                          ('the Flute',              'Save the duck and fly to freedom!', None, None, None),
    'Activated Flute':                ('the Flute',              'Save the duck and fly to freedom!', None, None, None),
    # One-off Unique Items
    'Book of Mudora':                 ('the Book',               'Hylian for Dingusses, 2nd Edition', None, 'This is a paradox?!', 'This is a paradox?!'),
    'Bug Catching Net':               ('the Bug Net',            "Let's catch some bees and faeries!", None, None, None),
    'Cane of Byrna':                  ('the Blue Cane',          'Use this to become invincible!', None, None, None),
    'Cane of Somaria':                ('the Red Cane',           'I make blocks to hold down switches!', None, None, None),
    'Cape':                           ('the Cape',               'Wear this to become invisible!', None, None, None),
    'Fire Rod':                       ('the Fire Rod',           "I'm the hot rod. I make things burn!", None, None, None),
    'Flippers':                       ('the Flippers',           'Fancy a swim?', None, 'The water is calm. Do you want to surf?', 'The water is calm. Do you want to surf?'),
    'Ice Rod':                        ('the Ice Rod',            "I'm the cold rod. I make things freeze!", None, None, None),
    'Hammer':                         ('the Hammer',             '       STOP!\nHammer time!', None, None, None),
    'Hookshot':                       ('the Hookshot',           'BOING!!!\n    BOING!!!\n        BOING!!!', None, None, None),
    'Lamp':                           ('the Lamp',               'Baby, baby, baby. Light my way!', None, None, None),
    'Magic Mirror':                   ('the Mirror',             "Isn't your reflection so pretty?", None, None, None),
    'Magic Powder':                   ('the Powder',             'You can turn anti-faeries into faeries', None, None, None),
    'Moon Pearl':                     ('the Moon Pearl',         'Bunny Link begone!', None, None, None),
    'Mushroom':                       ('the Mushroom',           "I'm a fun guy!\n\nI'm a funghi!", None, None, None),
    'Pegasus Boots':                  ('the Boots',              'Gotta go fast!', None, None, None),
    'Shovel':                         ('the Shovel',             'Can\n     You\n         Dig it?', None, None, None),
    # Upgrades
    'Magic Upgrade (1/2)':            ('a magic upgrade',        'Your magic power has been doubled!', None, None, None),
    'Magic Upgrade (1/4)':            ('a magic upgrade',        'Your magic power has been quadrupled!', None, None, None),
    'Bomb Upgrade (+5)':              ('bomb capacity',          'Increase bomb storage, low low price', None, None, None),
    'Bomb Upgrade (+10)':             ('bomb capacity',          'Increase bomb storage, low low price', None, None, None),
    'Arrow Upgrade (+5)':             ('arrow capacity',         'Increase arrow storage, low low price', None, None, None),
    'Arrow Upgrade (+10)':            ('arrow capacity',         'Increase arrow storage, low low price', None, None, None),
    # Heart Containers
    'Boss Heart Container':           ('a heart container',      'Maximum health increased! Yeah!', None, None, None),
    'Sanctuary Heart Container':      ('a heart container',      'Maximum health increased! Yeah!', None, None, None),
    'Piece of Heart':                 ('a piece of heart',       'Just a little piece of love!', None, None, None),
    # Junk Items
    'Single Arrow':                   ('an arrow',               'A lonely arrow sits here.', None, None, None),
    'Arrows (10)':                    ('ten arrows',             'This will give you ten shots with your bow!', None, None, None),
    'Single Bomb':                    ('a bomb',                 'I make things go BOOM! But just once.', None, None, None),
    'Bombs (3)':                      ('three bombs',            'I make things go triple BOOM!!!', None, None, None),
    'Bombs (10)':                     ('ten bombs',              'I make things go BOOM! Ten times!', None, None, None),
    'Rupee (1)':                      ('a green rupee',          'Just pocket change. Move right along.', None, None, None),
    'Rupees (5)':                     ('a blue rupee',           'Just pocket change. Move right along.', None, None, None),
    'Rupees (20)':                    ('a red rupee',            'Just couch cash. Move right along.', None, None, None),
    'Rupees (50)':                    ('fifty rupees',           'Just couch cash. Move right along.', None, None, None),
    'Rupees (100)':                   ('100 rupees',             'A rupee stash! Hell yeah!', None, None, None),
    'Rupees (300)':                   ('300 rupees',             'A rupee hoard! Hell yeah!', None, None, None),
    'Rupoor':                         ('a Rupoor',               'Pay me for the pedestal repair charge.', 'Pay me for the tablet repair charge.', None, None),
    'Small Heart':                    ('a recovery heart',       'Feeling affectionate today?', None, None, None),
    'Magic Jar':                      ('a magic refill',         'Watch your\nMagic Meter!', None, None, None),
    # Bottles
    'Bottle':                         ('a bottle',               'Now you can store potions and stuff!', None, None, None),
    'Bottle (Red Potion)':            ('a bottle',               'Hearty red goop!', None, None, None),
    'Bottle (Green Potion)':          ('a bottle',               'Refreshing green goop!', None, None, None),
    'Bottle (Blue Potion)':           ('a bottle',               'Delicious blue goop!', None, None, None),
    'Bottle (Fairy)':                 ('a bottle',               'Save me and I will revive you', None, None, None),
    'Bottle (Bee)':                   ('a bottle',               'I will sting your foes a few times', None, None, None),
    'Bottle (Good Bee)':              ('a bottle',               'I will sting your foes a whole lot!', None, None, None),
    'Red Potion':                     ('a red potion',           'Hearty red goop!', None, None, None),
    'Green Potion':                   ('a green potion',         'Refreshing green goop!', None, None, None),
    'Blue Potion':                    ('a blue potion',          'Delicious blue goop!', None, None, None),
    'Faerie':                         ('a fairy',                'Save me and I will revive you', None, None, None),
    'Bee':                            ('a bee',                  'I will sting your foes a few times', None, None, None),
    'Good Bee':                       ('a bee',                  'I will sting your foes a whole lot!', None, None, None),
    # Less Common Mode Items
    'Red Clock':                      ('a red clock',            'like the sands through a red hourglass', None, None, None),
    'Blue Clock':                     ('a blue clock',           'sapphire sand trickles down', None, None, None),
    'Green Clock':                    ('a green clock',          'time keeps on slipping,  slipping', None, None, None),
    'Apple':                          ('apples',                 "They're more like giant cherries…", None, None, None),
    'Bee Trap':                       ('Friendship',             'We will sting your face a whole lot!', None, None, None),
    'Single RNG':                     ('something new',          "something you don't yet have", None, None, None),
    'Multi RNG':                      ('something',              'something you may already have', None, None, None),
    # Free Small Keys
    'Small Key (Hyrule Castle)':      ('a small key to Hyrule Castle',      'A small key\nto the castle of Hyrule', None, None, None),
    'Small Key (Eastern Palace)':     ('a small key to Eastern Palace',     'A small key\nto the palace to the east', None, None, None),
    'Small Key (Desert Palace)':      ('a small key to Desert Palace',      'A small key\nto the palace in the desert', None, None, None),
    'Small Key (Tower of Hera)':      ('a small key to Tower of Hera',      'A small key\nto the tower of Moldorm', None, None, None),
    'Small Key (Agahnims Tower)':     ("a small key to Agahnim's Tower",    'A small key\nto the tower of Agahnim', None, None, None),
    'Small Key (Palace of Darkness)': ('a small key to Palace of Darkness', 'A small key\nto the Palace of Darkness', None, None, None),
    'Small Key (Swamp Palace)':       ('a small key to Swamp Palace',       'A small key\nto a waterlogged palace', None, None, None),
    'Small Key (Skull Woods)':        ('a small key to Skull Woods',        'A small key\nto the ghastly woods', None, None, None),
    'Small Key (Thieves Town)':       ("a small key to Thieves' Town",      'A small key\nto where thievery runs rampant', None, None, None),
    'Small Key (Ice Palace)':         ('a small key to Ice Palace',         'A small key\nto an Ice-cold palace', None, None, None),
    'Small Key (Misery Mire)':        ('a small key to Misery Mire',        'A small key\nto where Misery awaits you', None, None, None),
    'Small Key (Turtle Rock)':        ('a small key to Turtle Rock',        'A small key\nto the domain of turtles', None, None, None),
    'Small Key (Ganons Tower)':       ("a small key to Ganon's Tower",      'A small key\nto the most evil tower', None, None, None),
    'Small Key (Universal)':          ('a small key',                       'A small key\nto any door imaginable', None, None, None),
    # Free Big Keys
    'Big Key (Hyrule Castle)':        ('the Big Key of Hyrule Castle',      'The Big Key\nto the castle of Hyrule', None, None, None),
    'Big Key (Eastern Palace)':       ('the Big Key of Eastern Palace',     'The Big Key\nto the palace to the east', None, None, None),
    'Big Key (Desert Palace)':        ('the Big Key of Desert Palace',      'The Big Key\nto the palace in the desert', None, None, None),
    'Big Key (Tower of Hera)':        ('the Big Key of Tower of Hera',      'The Big Key\nto the tower of Moldorm', None, None, None),
    'Big Key (Agahnims Tower)':       ("the Big Key of Agahnim's Tower",    'The Big Key\nto the tower of Agahnim', None, None, None),
    'Big Key (Palace of Darkness)':   ('the Big Key of Palace of Darkness', 'The Big Key\nto the Palace of Darkness', None, None, None),
    'Big Key (Swamp Palace)':         ('the Big Key of Swamp Palace',       'The Big Key\nto a waterlogged palace', None, None, None),
    'Big Key (Skull Woods)':          ('the Big Key of Skull Woods',        'The Big Key\nto the ghastly woods', None, None, None),
    'Big Key (Thieves Town)':         ("the Big Key of Thieves' Town",      'The Big Key\nto where thievery runs rampant', None, None, None),
    'Big Key (Ice Palace)':           ('the Big Key of Ice Palace',         'The Big Key\nto an Ice-cold palace', None, None, None),
    'Big Key (Misery Mire)':          ('the Big Key of Misery Mire',        'The Big Key\nto where Misery awaits you', None, None, None),
    'Big Key (Turtle Rock)':          ('the Big Key of Turtle Rock',        'The Big Key\nto the domain of turtles', None, None, None),
    'Big Key (Ganons Tower)':         ("the Big Key of Ganon's Tower",      'The Big Key\nto the most evil tower', None, None, None),
    # Free Maps
    'Map (Hyrule Castle)':            ('the map of Hyrule Castle',          'A folded map\nto the castle of Hyrule', None, None, None),
    'Map (Eastern Palace)':           ('the map of Eastern Palace',         'A folded map\nto the palace to the east', None, None, None),
    'Map (Desert Palace)':            ('the map of Desert Palace',          'A folded map\nto the palace in the desert', None, None, None),
    'Map (Tower of Hera)':            ('the map of Tower of Hera',          'A folded map\nto the tower of Moldorm', None, None, None),
    'Map (Agahnims Tower)':           ("the map of Agahnim's Tower",        'A folded map\nto the tower of Agahnim', None, None, None),
    'Map (Palace of Darkness)':       ('the map of Palace of Darkness',     'A folded map\nto the Palace of Darkness', None, None, None),
    'Map (Swamp Palace)':             ('the map of Swamp Palace',           'A folded map\nto a waterlogged palace', None, None, None),
    'Map (Skull Woods)':              ('the map of Skull Woods',            'A folded map\nto the ghastly woods', None, None, None),
    'Map (Thieves Town)':             ("the map of Thieves' Town",          'A folded map\nto where thievery runs rampant', None, None, None),
    'Map (Ice Palace)':               ('the map of Ice Palace',             'A folded map\nto an Ice- cold palace', None, None, None),
    'Map (Misery Mire)':              ('the map of Misery Mire',            'A folded map\nto where Misery awaits you', None, None, None),
    'Map (Turtle Rock)':              ('the map of Turtle Rock',            'A folded map\nto the domain of turtles', None, None, None),
    'Map (Ganons Tower)':             ("the map of Ganon's Tower",          'A folded map\nto the most evil tower', None, None, None),
    # Free Compasses
    'Compass (Hyrule Castle)':        ('the compass of Hyrule Castle',      'Compass was defective. Bad seller, 0 out of 10.', None, None, None),
    'Compass (Eastern Palace)':       ('the compass of Eastern Palace',     'Now you can find\nArmos Knights!', None, None, None),
    'Compass (Desert Palace)':        ('the compass of Desert Palace',      'Now you can find\nLanmolas!', None, None, None),
    'Compass (Tower of Hera)':        ('the compass of Tower of Hera',      'Now you can find\nMoldorm!', None, None, None),
    'Compass (Agahnims Tower)':       ("the compass of Agahnim's Tower",    'Now you can find\nAgahnim!', None, None, None),
    'Compass (Palace of Darkness)':   ('the compass of Palace of Darkness', 'Now you can find\nHelmasaur King!', None, None, None),
    'Compass (Swamp Palace)':         ('the compass of Swamp Palace',       'Now you can find\nArrghus!', None, None, None),
    'Compass (Skull Woods)':          ('the compass of Skull Woods',        'Now you can find\nMothula!', None, None, None),
    'Compass (Thieves Town)':         ("the compass of Thieves' Town",      'Now you can find\nBlind!', None, None, None),
    'Compass (Ice Palace)':           ('the compass of Ice Palace',         'Now you can find\nKholdstare!', None, None, None),
    'Compass (Misery Mire)':          ('the compass of Misery Mire',        'Now you can find\nVitreous!', None, None, None),
    'Compass (Turtle Rock)':          ('the compass of Turtle Rock',        'Now you can find\nTrinexx!', None, None, None),
    'Compass (Ganons Tower)':         ("the compass of Ganon's Tower",      'Now you can find\nAgahnim… again!', None, None, None),
    # Goal Items
    'Triforce':                       ('the Triforce',     'You found the goal…', 'You found the goal…', '\n  ~ YOU WIN! ~', '\n  ~ YOU WIN! ~'),
    'Power Star':                     ('a Power Star',     "Aim for the moon. You may hit a 'star'", "Watch for falling stars", None, None),
    'Triforce Piece':                 ('a Triforce Piece', "Please don't eat the shiny golden dorito.", "Watch for falling triangles", None, None),
}

# Pedestal, Sick Kid, Zora, Potion Ship, Flute Spot, Link's Uncle
item_credit_text = {
    'Nothing':                        ('and the hot air',       'the zen kid',         'outright theft',        'shroom theft',             'empty boy is bored again',         'your uncle has nothing'),
    # Swords
    'Fighter Sword & Shield':         ('the sword and shield',  'monster-hunting kid', 'tiny sword for sale',   'fungus for tiny slasher',  'sword boy fights again',           'your uncle recovers'),
    'Fighter Sword':                  ('and the tiny sword',    'sword-wielding kid',  'tiny sword for sale',   'fungus for tiny slasher',  'sword boy fights again',           'your uncle recovers'),
    'Master Sword':                   ('and the master sword',  'sword-wielding kid',  'glow sword for sale',   'fungus for blue slasher',  'sword boy fights again',           'your uncle recovers'),
    'Tempered Sword':                 ('and the tempered sword','sword-wielding kid',  'flame sword for sale',  'fungus for red slasher',   'sword boy fights again',           'your uncle recovers'),
    'Golden Sword':                   ('and the butter sword',  'sword-wielding kid',  'butter for sale',       'cap churned to butter',    'sword boy fights again',           'your uncle recovers'),
    'Progressive Sword':              ('and the new sword',     'sword-wielding kid',  'sword for sale',        'fungus for some slasher',  'sword boy fights again',           'your uncle recovers'),
    # Shields
    'Blue Shield':                    ('and the stone blocker', 'shield-wielding kid', 'shield for sale',       'fungus for shield',        'shield boy defends again',         'your uncle protects'),
    'Red Shield':                     ('and the shot blocker',  'shield-wielding kid', 'fire shield for sale',  'fungus for fire shield',   'shield boy defends again',         'your uncle protects'),
    'Mirror Shield':                  ('and the laser blocker', 'shield-wielding kid', 'face shield for sale',  'fungus for face shield',   'shield boy defends again',         'your uncle protects'),
    'Progressive Shield':             ('and the new blocker',   'shield-wielding kid', 'shield for sale',       'fungus for shield',        'shield boy defends again',         'your uncle protects'),
    # Mail / Armor
    'Blue Mail':                      ('and the banana hat',    'the protected kid',   'banana hat for sale',   'the clothing store',       'tailor boy banana hatted again',   'your uncle tailors'),
    'Red Mail':                       ('and the eggplant hat',  'well-protected kid',  'purple hat for sale',   'the nice clothing store',  'tailor boy fears nothing again',   'your uncle tailors'),
    'Progressive Mail':               ('and the fancy hat',     'the protected kid',   'new hat for sale',      'the clothing store',       'tailor boy has threads again',     'your uncle tailors'),
    # Gloves
    'Power Glove':                    ('and the grey mittens',  'body-building kid',   'lift glove for sale',   'fungus for gloves',        'body-building boy lifts again',    'your uncle goes to the gym'),
    'Titans Mitts':                   ('and the golden glove',  'body-building kid',   'carry glove for sale',  'fungus for bling-gloves',  'body-building boy has gold again', 'your uncle goes to the gym'),
    'Progressive Glove':              ('and the lift upgrade',  'body-building kid',   'some glove for sale',   'fungus for gloves',        'body-building boy lifts again',    'your uncle goes to the gym'),
    # Bow
    'Bow':                            ('the stick and twine',   'arrow-slinging kid',  'arrow sling for sale',  'witch and robin hood',     'archer boy shoots again',          'your uncle, robin hood'),
    'Progressive Bow':                ('the stick and twine',   'arrow-slinging kid',  'arrow sling for sale',  'witch and robin hood',     'archer boy shoots again',          'your uncle, robin hood'),
    'Progressive Bow (Alt)':          ('the stick and twine',   'arrow-slinging kid',  'arrow sling for sale',  'witch and robin hood',     'archer boy shoots again',          'your uncle, robin hood'),
    'Silver Bow':                     ('and the baconmaker',    'ganon-killing kid',   'ganon doom for sale',   'fungus for pork',          'archer boy shines again',          'your uncle makes bacon'),
    'Silver Arrows':                  ('and the baconmaker',    'ganon-killing kid',   'ganon doom for sale',   'fungus for pork',          'archer boy shines again',          'your uncle makes bacon'),
    # Medallions
    'Bombos':                         ('and the swirly coin',   'coin-collecting kid', 'swirly coin for sale',  'shrooms for swirly-coin',  'medallion boy melts room again',   'your uncle collects coins'),
    'Ether':                          ('and the bolt coin',     'coin-collecting kid', 'bolt coin for sale',    'shrooms for bolt-coin',    'medallion boy sees floor again',   'your uncle collects coins'),
    'Quake':                          ('and the wavy coin',     'coin-collecting kid', 'wavy coin for sale',    'shrooms for wavy-coin',    'medallion boy shakes dirt again',  'your uncle collects coins'),
    # Boomerangs
    'Blue Boomerang':                 ('and the bluemarang',    'the bat-throwing kid','bent stick for sale',   'fungus for puma-stick',    'throwing boy plays fetch again',   'your uncle returns'),
    'Red Boomerang':                  ('and the badmarang',     'the bat-throwing kid','air foil for sale',     'fungus for return-stick',  'magical boy plays fetch again',    'your uncle returns'),
    # Flutes
    'Flute':                          ('and the duck call',     'the duck-call kid',   'duck call for sale',    'duck-calls for trade',     'ocarina boy plays again',          'your uncle trains ducks'),
    'Activated Flute':                ('and the duck call',     'the duck-call kid',   'duck call for sale',    'duck-calls for trade',     'ocarina boy plays again',          'your uncle trains ducks'),
    # One-off Unique Items
    'Book of Mudora':                 ('and the story book',    'the scholarly kid',   'moon runes for sale',   'drugs for literacy',       'book-worm boy can read again',     'your uncle can read'),
    'Bug Catching Net':               ('and the bee catcher',   'the bug-catching kid','stick web for sale',    'fungus for butterflies',   'wrong boy catches bees again',     'your uncle catches bees'),
    'Cane of Byrna':                  ('and the walking stick', 'the spark-making kid','spark stick for sale',  'spark-stick for trade',    'cane boy encircles again',         'your uncle sparks'),
    'Cane of Somaria':                ('and the block stick',   'the block-making kid','block stick for sale',  'block stick for trade',    'cane boy makes blocks again',      'your uncle makes blocks'),
    'Cape':                           ('the camouflage cape',   'red riding-hood kid', 'red hood for sale',     'hood from a hood',         'dapper boy hides again',           'your uncle can hide'),
    'Fire Rod':                       ('and the flamethrower',  'fire-starting kid',   'rage rod for sale',     'fungus for rage-rod',      'firestarter boy burns again',      'your uncle, the arsonist'),
    'Flippers':                       ('and the toewebs',       'the swimming kid',    'finger webs for sale',  'shrooms let you swim',     'swimming boy swims again',         'your uncle can swim'),
    'Ice Rod':                        ('and the freeze ray',    'the ice-bending kid', 'freeze ray for sale',   'fungus for ice-rod',       'ice-cube boy freezes again',       'your uncle is cool'),
    'Hammer':                         ('and m.c.hammer',        'hammer-smashing kid', 'm.c.hammer for sale',   'stop...   hammer time',    'stop, hammer time',                'your uncle, m.c.hammer'),
    'Hookshot':                       ('and the tickle beam',   'tickle-monster kid',  'tickle beam for sale',  'witch and tickle boy',     'beam boy tickles again',           'your uncle goes BOING'),
    'Lamp':                           ('and the flashlight',    'light-shining kid',   'flashlight for sale',   'fungus for illumination',  'illuminated boy can see again',    'your uncle lights the way'),
    'Magic Mirror':                   ('and the face reflector','the narcissistic kid','your face for sale',    'trades looking-glass',     'narcissistic boy is happy again',  'your uncle is vain'),
    'Magic Powder':                   ('and the magic sack',    'the sack-holding kid','magic sack for sale',   'the witch and assistant',  'magic boy plays marbles again',    'your uncle and his sack'),
    'Moon Pearl':                     ('and the jaw breaker',   'fortune-telling kid', 'lunar orb for sale',    'shrooms for moon rock',    'moon boy plays ball again',        'your uncle shoots marbles'),
    'Mushroom':                       ('and the legal drugs',   'the drug-dealing kid','legal drugs for sale',  'shroom swap',              'shroom boy sells drugs again',     'your uncle deals drugs'),
    'Pegasus Boots':                  ('and the sprint shoes',  'the running-man kid', 'sprint shoe for sale',  'shrooms for speed',        'gotta-go-fast boy runs again',     'your uncle goes fast'),
    'Shovel':                         ('and the spade',         'archaeologist kid',   'dirt spade for sale',   'can you dig it',           'shovel boy digs again',            'your uncle can dig it'),
    # Upgrades
    'Magic Upgrade (1/2)':            ('and the spell power',   'the magic-saving kid','wizardry for sale',     'mekalekahi mekahiney ho',  'magic boy saves magic again',      'your uncle is magical'),
    'Magic Upgrade (1/4)':            ('and the spell power',   'the magic-saving kid','wizardry for sale',     'mekalekahi mekahiney ho',  'magic boy saves magic again',      'your uncle is magical'),
    'Bomb Upgrade (+5)':              ('and the bomb bag',      'boom-enlarging kid',  'bomb boost for sale',   'the shroom goes boom',     'upgrade boy explodes more again',  'your uncle wants more bombs'),
    'Bomb Upgrade (+10)':             ('and the bomb bag',      'boom-enlarging kid',  'bomb boost for sale',   'the shroom goes boom',     'upgrade boy explodes more again',  'your uncle wants more bombs'),
    'Arrow Upgrade (+5)':             ('and the quiver',        'quiver-enlarging kid','arrow boost for sale',  'witch and more skewers',   'upgrade boy sews more again',      'your uncle wants more arrows'),
    'Arrow Upgrade (+10)':            ('and the quiver',        'quiver-enlarging kid','arrow boost for sale',  'witch and more skewers',   'upgrade boy sews more again',      'your uncle wants more arrows'),
    # Heart Containers
    'Boss Heart Container':           ('and the full heart',    'the life-giving kid', 'love for sale',         'fungus for life',          'life boy feels love again',        'your uncle is healthy'),
    'Sanctuary Heart Container':      ('and the full heart',    'the life-giving kid', 'love for sale',         'fungus for life',          'life boy feels love again',        'your uncle is healthy'),
    'Piece of Heart':                 ('and the broken heart',  'the life-giving kid', 'little love for sale',  'fungus for life',          'life boy feels some love again',   'your uncle is healthy'),
    # Junk Items
    'Single Arrow':                   ('and the arrow',         'stick-collecting kid','sewing needle for sale','fungus for arrow',         'archer boy sews again',            'your uncle sews'),
    'Arrows (10)':                    ('and the arrow pack',    'stick-collecting kid','sewing kit for sale',   'fungus for arrows',        'archer boy sews again',            'your uncle sews'),
    'Single Bomb':                    ('and the explosion',     'the bomb-holding kid','firecracker for sale',  'blend fungus into bomb',   "'splosion boy explodes again",     'your uncle demolishes'),
    'Bombs (3)':                      ('and the explosions',    'the bomb-holding kid','firecrackers for sale', 'blend fungus into bombs',  "'splosion boy explodes again",     'your uncle demolishes'),
    'Bombs (10)':                     ('and the explosions',    'the bomb-holding kid','firecrackers for sale', 'blend fungus into bombs',  "'splosion boy explodes again",     'your uncle demolishes'),
    'Rupee (1)':                      ('and the pocket change', 'poverty-struck kid',  'life lesson for sale',  'buying cheap drugs',       'destitute boy has snack again',    'your uncle is broke'),
    'Rupees (5)':                     ('and the pocket change', 'poverty-struck kid',  'life lesson for sale',  'buying cheap drugs',       'destitute boy has snack again',    'your uncle is broke'),
    'Rupees (20)':                    ('and the couch cash',    'the piggy-bank kid',  'life lesson for sale',  'the witch buying drugs',   'destitute boy has lunch again',    'your uncle is broke'),
    'Rupees (50)':                    ('and the couch cash',    'the well-off kid',    'life lesson for sale',  'buying okay drugs',        'destitute boy has dinner again',   'your uncle is broke'),
    'Rupees (100)':                   ('and the rupee stash',   'the kind-of-rich kid','life lesson for sale',  'buying good drugs',        'affluent boy goes drinking again', 'your uncle is rich'),
    'Rupees (300)':                   ('and the rupee hoard',   'the really-rich kid', 'life lesson for sale',  'buying the best drugs',    'fat-cat boy is rich again',        'your uncle is rich'),
    'Rupoor':                         ('and the toll-booth',    'the toll-booth kid',  'double loss for sale',  'witch stole your rupees',  'affluent boy steals rupees again', 'your uncle is a thief'),
    'Small Heart':                    ('and the tiny heart',    'affection-giving kid','affection for sale',    'i heart shrooms',          'loving boy has affection again',   'your uncle is creepy'),
    'Magic Jar':                      ('and the fancy pottery', 'the ceramics kid',    'playing pot of greed',  'shrooms in a jar',         'clay-working boy has magic again', 'your uncle likes ceramics'),
    # Bottles
    'Bottle':                         ('and the terrarium',     'the terrarium kid',   'terrarium for sale',    'special promotion',        'bottle boy has terrarium again',   'your uncle likes turtles'),
    'Bottle (Red Potion)':            ('and the red goo',       'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has red goo again',     'your uncle helps out'),
    'Bottle (Green Potion)':          ('and the green goo',     'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has green goo again',   'your uncle helps out'),
    'Bottle (Blue Potion)':           ('and the blue goo',      'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has blue goo again',    'your uncle helps out'),
    'Bottle (Fairy)':                 ('and the captive',       'the tingle kid',      'hostage for sale',      'fairy dust and shrooms',   'bottle boy has friend again',      'your uncle has a friend'),
    'Bottle (Bee)':                   ('and the sting buddy',   'the beekeeper kid',   'insect for sale',       'shroom pollenation',       'bottle boy has mad bee again',     'your uncle, the beekeeper'),
    'Bottle (Good Bee)':              ('and the sparkle sting', 'the beekeeper kid',   'insect for sale',       'shroom pollenation',       'bottle boy has beetor again',      'your uncle, the beekeeper'),
    'Red Potion':                     ('and the red goo',       'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has red goo again',     'your uncle helps out'),
    'Green Potion':                   ('and the green goo',     'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has green goo again',   'your uncle helps out'),
    'Blue Potion':                    ('and the blue goo',      'the liquid kid',      'potion for sale',       'free samples',             'bottle boy has blue goo again',    'your uncle helps out'),
    'Faerie':                         ('and the captive',       'the tingle kid',      'hostage for sale',      'fairy dust and shrooms',   'bottle boy has friend again',      'your uncle has a friend'),
    'Bee':                            ('and the sting buddy',   'the beekeeper kid',   'insect for sale',       'shroom pollenation',       'bottle boy has mad bee again',     'your uncle, the beekeeper'),
    'Good Bee':                       ('and the sparkle sting', 'the beekeeper kid',   'insect for sale',       'shroom pollenation',       'bottle boy has beetor again',      'your uncle, the beekeeper'),
    # Less Common Mode Items
    'Red Clock':                      ('and the timepiece',     'the ruby-time kid',   'ruby time for sale',    'travel time with shrooms', 'moment boy travels time again',    'your uncle time travels'),
    'Blue Clock':                     ('and the timepiece',     'sapphire-time kid',   'sapphire time for sale','travel time with shrooms', 'moment boy time travels again',    'your uncle time travels'),
    'Green Clock':                    ('and the timepiece',     'the emerald-time kid','emerald time for sale', 'travel time with shrooms', 'moment boy adjusts time again',    'your uncle time travels'),
    'Apple':                          ('and the apple tree',    'the orchard kid',     'apples for sale',       'fungus to apples',         'farmer boy picks apples again',    'your uncle, the farmer'),
    'Bee Trap':                       ('and the sting buddies', 'the beekeeper kid',   'insects for sale',      'shroom pollenation',       'bottle boy has mad bees again',    'six bees in a trenchcoat'),
    'Single RNG':                     ('and the mystery',       'the mysterious kid',  'total mystery for sale','fungus for something',     'unknown boy somethings again',     "your uncle doesn't know"),
    'Multi RNG':                      ('and the mystery',       'the mysterious kid',  'total mystery for sale','fungus for something',     'unknown boy somethings again',     "your uncle doesn't know"),
    # Free Small Keys
    'Small Key (Hyrule Castle)':      ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Eastern Palace)':     ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Desert Palace)':      ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Tower of Hera)':      ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Agahnims Tower)':     ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Palace of Darkness)': ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Swamp Palace)':       ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Skull Woods)':        ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Thieves Town)':       ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Ice Palace)':         ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Misery Mire)':        ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Turtle Rock)':        ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Ganons Tower)':       ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    'Small Key (Universal)':          ('and the key',           'the unlocking kid',   'keys for sale',         'unlock the fungus',        'key boy opens door again',         'your uncle picks locks'),
    # Free Big Keys
    'Big Key (Hyrule Castle)':        ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Eastern Palace)':       ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Desert Palace)':        ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Tower of Hera)':        ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Agahnims Tower)':       ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Palace of Darkness)':   ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Swamp Palace)':         ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Skull Woods)':          ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Thieves Town)':         ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Ice Palace)':           ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Misery Mire)':          ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Turtle Rock)':          ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    'Big Key (Ganons Tower)':         ('and the master key',    'the big-unlock kid',  'big key for sale',      'face key fungus',          'key boy opens chest again',        'your uncle opens chests'),
    # Free Maps
    'Map (Hyrule Castle)':            ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Eastern Palace)':           ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Desert Palace)':            ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Tower of Hera)':            ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Agahnims Tower)':           ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Palace of Darkness)':       ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Swamp Palace)':             ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Skull Woods)':              ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Thieves Town)':             ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Ice Palace)':               ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Misery Mire)':              ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Turtle Rock)':              ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    'Map (Ganons Tower)':             ('and the guide paper',   'cartography kid',     'fancy paper for sale',  'a map to shrooms',         'map boy navigates again',          'your uncle, the cartographer'),
    # Free Compasses
    'Compass (Hyrule Castle)':        ('and the broken magnet', 'the lost kid',        'water-damaged compass', 'magnets, how do they work','compass boy finds nothing again',  'your uncle is lost'),
    'Compass (Eastern Palace)':       ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Desert Palace)':        ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Tower of Hera)':        ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Agahnims Tower)':       ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Palace of Darkness)':   ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Swamp Palace)':         ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Skull Woods)':          ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Thieves Town)':         ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Ice Palace)':           ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Misery Mire)':          ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Turtle Rock)':          ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    'Compass (Ganons Tower)':         ('and the boss pointer',  'the magnetic kid',    'compass for sale',      'magnetic fungus',          'compass boy finds boss again',     'your uncle is magnetic'),
    # Goal Items
    'Triforce':                       ('and the triforce',      'victorious kid',      'victory for sale',      'fungus for the win',       'greedy boy wins game again',       'your uncle steals the show'),
    'Power Star':                     ('and the power star',    'star-struck kid',     'star for sale',         'see stars with shroom',    'mario powers up again',            'your uncle, mario'),
    'Triforce Piece':                 ('and the piece of power','triangular kid',      'triangle for sale',     'fungus for triangle',      'wise boy has triangle again',      'your uncle is wise'),
}

# Advancement, Type, ItemCode
# This should correspond to every item in the game that we can possibly send or acquire.
# It is okay for entries in this table to not have hints above.
item_table = {
    'Nothing':                        (False, None, 0x5A),
    # Swords
    'Fighter Sword & Shield':         (True, 'Sword', 0x00), # Vanilla uncle item, not in Archipelago
    'Fighter Sword':                  (True, 'Sword', 0x49),
    'Master Sword':                   (True, 'Sword', 0x50),
    'Tempered Sword':                 (True, 'Sword', 0x02),
    'Golden Sword':                   (True, 'Sword', 0x03),
    'Progressive Sword':              (True, 'Sword', 0x5E),
    # Shields
    'Blue Shield':                    (False, None, 0x04),
    'Red Shield':                     (False, None, 0x05),
    'Mirror Shield':                  (True, None, 0x06),
    'Progressive Shield':             (True, None, 0x5F),
    # Mail / Armor
    'Blue Mail':                      (False, None, 0x22),
    'Red Mail':                       (False, None, 0x23),
    'Progressive Mail':               (False, None, 0x60),
    # Gloves
    'Power Glove':                    (True, None, 0x1B),
    'Titans Mitts':                   (True, None, 0x1C),
    'Progressive Glove':              (True, None, 0x61),
    # Bow
    'Bow':                            (True, None, 0x0B),
    'Progressive Bow':                (True, None, 0x64),
    'Progressive Bow (Alt)':          (True, None, 0x65),
    'Silver Bow':                     (True, None, 0x3B),
    'Silver Arrows':                  (True, None, 0x58), # Legacy Silver Arrows, you know, the ones with 'Ag' on the sprite
    # Medallions
    'Bombos':                         (True, None, 0x0F),
    'Ether':                          (True, None, 0x10),
    'Quake':                          (True, None, 0x11),
    # Boomerangs
    'Blue Boomerang':                 (True, None, 0x0C),
    'Red Boomerang':                  (True, None, 0x2A),
    # Flutes
    'Flute':                          (True, None, 0x14),
    'Activated Flute':                (True, None, 0x4A), # Pre-activated, unsure if it works in item form but works in startinventory
    # One-off Unique Items
    'Book of Mudora':                 (True, None, 0x1D),
    'Bug Catching Net':               (True, None, 0x21),
    'Cane of Byrna':                  (True, None, 0x18),
    'Cane of Somaria':                (True, None, 0x15),
    'Cape':                           (True, None, 0x19),
    'Fire Rod':                       (True, None, 0x07),
    'Flippers':                       (True, None, 0x1E),
    'Ice Rod':                        (True, None, 0x08),
    'Hammer':                         (True, None, 0x09),
    'Hookshot':                       (True, None, 0x0A),
    'Lamp':                           (True, None, 0x12),
    'Magic Mirror':                   (True, None, 0x1A),
    'Magic Powder':                   (True, None, 0x0D),
    'Moon Pearl':                     (True, None, 0x1F),
    'Mushroom':                       (True, None, 0x29),
    'Pegasus Boots':                  (True, None, 0x4B),
    'Shovel':                         (True, None, 0x13),
    # Upgrades
    'Magic Upgrade (1/2)':            (True, None, 0x4E),
    'Magic Upgrade (1/4)':            (True, None, 0x4F),
    'Bomb Upgrade (+5)':              (False, None, 0x51),
    'Bomb Upgrade (+10)':             (False, None, 0x52),
    'Arrow Upgrade (+5)':             (False, None, 0x53),
    'Arrow Upgrade (+10)':            (False, None, 0x54),
    # Heart Containers
    'Boss Heart Container':           (False, None, 0x3E),
    'Sanctuary Heart Container':      (False, None, 0x3F),
    'Piece of Heart':                 (False, None, 0x17),
    # Junk Items
    'Single Arrow':                   (False, 'Junk', 0x43),
    'Arrows (10)':                    (False, 'Junk', 0x44),
    'Single Bomb':                    (False, 'Junk', 0x27),
    'Bombs (3)':                      (False, 'Junk', 0x28),
    'Bombs (10)':                     (False, 'Junk', 0x31),
    'Rupee (1)':                      (False, 'Junk', 0x34),
    'Rupees (5)':                     (False, 'Junk', 0x35),
    'Rupees (20)':                    (False, 'Junk', 0x36),
    'Rupees (50)':                    (False, 'Junk', 0x41),
    'Rupees (100)':                   (False, 'Junk', 0x40),
    'Rupees (300)':                   (False, 'Junk', 0x46),
    'Rupoor':                         (False, 'Junk', 0x59),
    'Small Heart':                    (False, 'Junk', 0x42), # Works in chests just fine
    'Magic Jar':                      (False, 'Junk', 0xB3), # Works in chests just fine (after baserom update)
    # Bottles
    'Bottle':                         (True, None, 0x16),
    'Bottle (Red Potion)':            (True, None, 0x2B),
    'Bottle (Green Potion)':          (True, None, 0x2C),
    'Bottle (Blue Potion)':           (True, None, 0x2D),
    'Bottle (Fairy)':                 (True, None, 0x3D),
    'Bottle (Bee)':                   (True, None, 0x3C),
    'Bottle (Good Bee)':              (True, None, 0x48),
    'Red Potion':                     (False, None, 0x2E), # Goes into an empty bottle?
    'Green Potion':                   (False, None, 0x2F), # Goes into an empty bottle?
    'Blue Potion':                    (False, None, 0x30), # Goes into an empty bottle?
    'Faerie':                         (False, None, 0xB1), # Spawns fairy atop player
    'Bee':                            (False, None, 0x0E), # Goes into an empty bottle
    'Good Bee':                       (False, None, 0xB2), # Untested?
    # Less Common Mode Items
    'Red Clock':                      (False, None, 0x5B),
    'Blue Clock':                     (False, None, 0x5C),
    'Green Clock':                    (False, None, 0x5D),
    'Apple':                          (False, None, 0xB4), # Spawns a burst of apples over the player
    'Bee Trap':                       (False, None, 0xB0), # Spawns a burst of bees over the player
    'Single RNG':                     (False, None, 0x62), # Never once tested this in my life
    'Multi RNG':                      (False, None, 0x63), # Never once tested this in my life
    #'Hint':                           (False, None, 0xB5), # Commented out in vanilla Archipelago, probably nonfunctional
    #'Bomb Trap':                      (False, None, 0xB6), # Commented out in vanilla Archipelago, probably nonfunctional
    # Free Small Keys
    'Small Key (Hyrule Castle)':      (False, 'SmallKey', 0xA0),
    'Small Key (Eastern Palace)':     (False, 'SmallKey', 0xA2),
    'Small Key (Desert Palace)':      (False, 'SmallKey', 0xA3),
    'Small Key (Tower of Hera)':      (False, 'SmallKey', 0xAA),
    'Small Key (Agahnims Tower)':     (False, 'SmallKey', 0xA4),
    'Small Key (Palace of Darkness)': (False, 'SmallKey', 0xA6),
    'Small Key (Swamp Palace)':       (False, 'SmallKey', 0xA5),
    'Small Key (Skull Woods)':        (False, 'SmallKey', 0xA8),
    'Small Key (Thieves Town)':       (False, 'SmallKey', 0xAB),
    'Small Key (Ice Palace)':         (False, 'SmallKey', 0xA9),
    'Small Key (Misery Mire)':        (False, 'SmallKey', 0xA7),
    'Small Key (Turtle Rock)':        (False, 'SmallKey', 0xAC),
    'Small Key (Ganons Tower)':       (False, 'SmallKey', 0xAD),
    'Small Key (Universal)':          (False, None, 0xAF),
    # Free Big Keys
    'Big Key (Hyrule Castle)':        (False, 'BigKey', 0x9F),
    'Big Key (Eastern Palace)':       (False, 'BigKey', 0x9D),
    'Big Key (Desert Palace)':        (False, 'BigKey', 0x9C),
    'Big Key (Tower of Hera)':        (False, 'BigKey', 0x95),
    'Big Key (Agahnims Tower)':       (False, 'BigKey', 0x9B), # does not exist in main branch baserom
    'Big Key (Palace of Darkness)':   (False, 'BigKey', 0x99),
    'Big Key (Swamp Palace)':         (False, 'BigKey', 0x9A),
    'Big Key (Skull Woods)':          (False, 'BigKey', 0x97),
    'Big Key (Thieves Town)':         (False, 'BigKey', 0x94),
    'Big Key (Ice Palace)':           (False, 'BigKey', 0x96),
    'Big Key (Misery Mire)':          (False, 'BigKey', 0x98),
    'Big Key (Turtle Rock)':          (False, 'BigKey', 0x93),
    'Big Key (Ganons Tower)':         (False, 'BigKey', 0x92),
    # Free Maps
    'Map (Hyrule Castle)':            (False, 'Map', 0x7F),
    'Map (Eastern Palace)':           (False, 'Map', 0x7D),
    'Map (Desert Palace)':            (False, 'Map', 0x7C),
    'Map (Tower of Hera)':            (False, 'Map', 0x75),
    'Map (Agahnims Tower)':           (False, 'Map', 0x7B), # does not exist in main branch baserom
    'Map (Palace of Darkness)':       (False, 'Map', 0x79),
    'Map (Swamp Palace)':             (False, 'Map', 0x7A),
    'Map (Skull Woods)':              (False, 'Map', 0x77),
    'Map (Thieves Town)':             (False, 'Map', 0x74),
    'Map (Ice Palace)':               (False, 'Map', 0x76),
    'Map (Misery Mire)':              (False, 'Map', 0x78),
    'Map (Turtle Rock)':              (False, 'Map', 0x73),
    'Map (Ganons Tower)':             (False, 'Map', 0x72),
    # Free Compasses
    'Compass (Hyrule Castle)':        (False, 'Compass', 0x8F),
    'Compass (Eastern Palace)':       (False, 'Compass', 0x8D),
    'Compass (Desert Palace)':        (False, 'Compass', 0x8C),
    'Compass (Tower of Hera)':        (False, 'Compass', 0x85),
    'Compass (Agahnims Tower)':       (False, 'Compass', 0x8B), # does not exist in main branch baserom
    'Compass (Palace of Darkness)':   (False, 'Compass', 0x89),
    'Compass (Swamp Palace)':         (False, 'Compass', 0x8A),
    'Compass (Skull Woods)':          (False, 'Compass', 0x87),
    'Compass (Thieves Town)':         (False, 'Compass', 0x84),
    'Compass (Ice Palace)':           (False, 'Compass', 0x86),
    'Compass (Misery Mire)':          (False, 'Compass', 0x88),
    'Compass (Turtle Rock)':          (False, 'Compass', 0x83),
    'Compass (Ganons Tower)':         (False, 'Compass', 0x82),
    # Goal Items
    'Triforce':                       (True, None, 0x6A), # Instant win game
    'Power Star':                     (True, None, 0x6B), # Alternative triforce hunt piece
    'Triforce Piece':                 (True, None, 0x6C),
    # Prizes
    'Red Pendant':                    (True, 'Crystal', (0x01, 0x32, 0x60, 0x00, 0x69, 0x03)),
    'Green Pendant':                  (True, 'Crystal', (0x04, 0x38, 0x62, 0x00, 0x69, 0x01)),
    'Blue Pendant':                   (True, 'Crystal', (0x02, 0x34, 0x60, 0x00, 0x69, 0x02)),
    'Crystal 1':                      (True, 'Crystal', (0x02, 0x34, 0x64, 0x40, 0x7F, 0x06)),
    'Crystal 2':                      (True, 'Crystal', (0x10, 0x34, 0x64, 0x40, 0x79, 0x06)),
    'Crystal 3':                      (True, 'Crystal', (0x40, 0x34, 0x64, 0x40, 0x6C, 0x06)),
    'Crystal 4':                      (True, 'Crystal', (0x20, 0x34, 0x64, 0x40, 0x6D, 0x06)),
    'Crystal 5':                      (True, 'Crystal', (0x04, 0x32, 0x64, 0x40, 0x6E, 0x06)),
    'Crystal 6':                      (True, 'Crystal', (0x01, 0x32, 0x64, 0x40, 0x6F, 0x06)),
    'Crystal 7':                      (True, 'Crystal', (0x08, 0x34, 0x64, 0x40, 0x7C, 0x06)),
    # Fake event "items"
    'Beat Agahnim 1':                 (True, 'Event', None),
    'Beat Agahnim 2':                 (True, 'Event', None),
    'Get Frog':                       (True, 'Event', None),
    'Return Smith':                   (True, 'Event', None),
    'Pick Up Purple Chest':           (True, 'Event', None),
    'Open Floodgate':                 (True, 'Event', None),
    'Trench 1 Filled':                (True, 'Event', None), # Event only used in doors branch
    'Trench 2 Filled':                (True, 'Event', None), # Event only used in doors branch
    'Drained Swamp':                  (True, 'Event', None), # Event only used in doors branch
    'Shining Light':                  (True, 'Event', None), # Event only used in doors branch
    'Maiden Rescued':                 (True, 'Event', None), # Event only used in doors branch
    'Maiden Unmasked':                (True, 'Event', None), # Event only used in doors branch
    'Convenient Block':               (True, 'Event', None), # Event only used in doors branch
    'Zelda Herself':                  (True, 'Event', None), # Event only used in doors branch
    'Zelda Delivered':                (True, 'Event', None), # Event only used in doors branch
}

lookup_id_to_name = {data[2]: name for name, data in item_table.items()}

hint_blacklist = {"Triforce"}

item_name_groups = {
    "Bows": {"Bow", "Silver Arrows", "Silver Bow", "Progressive Bow (Alt)", "Progressive Bow"},
    "Gloves": {"Power Glove", "Progressive Glove", "Titans Mitts"},
    "Medallions": {"Ether", "Bombos", "Quake"}
}

# generic groups, (Name, substring)
_simple_groups = {
    ("Swords", "Sword"),
    ("Shields", "Shield"),
    ("Mails", "Mail"),

    ("Boomerangs", "Boomerang"),
    ("Rods", "Rod"),
    ("Canes", "Cane"),

    ("Upgrades", "Upgrade"), # Capacity and Magic Upgrades

    ("Small Keys", "Small Key"),
    ("Big Keys", "Big Key"),
    ("Compasses", "Compass"),
    ("Maps", "Map"),

    ("Bottles", "Bottle"),
    ("Potions", "Potion"),
    ("Rupees", "Rupee"),
    ("Clocks", "Clock"),

    ("Crystals", "Crystal"),
    ("Pendants", "Pendant")
}

for basename, substring in _simple_groups:
    tempset = item_name_groups[basename] = set()
    for itemname in item_table:
        if substring in itemname:
            tempset.add(itemname)

del (_simple_groups)

progression_items = {name for name, data in item_table.items() if type(data[2]) == int and data[0]}
item_name_groups['Everything'] = {name for name, data in item_table.items() if type(data[2]) == int}
item_name_groups['Progression Items'] = progression_items
item_name_groups['Non Progression Items'] = item_name_groups['Everything'] - progression_items

trap_replaceable = item_name_groups['Rupees'] | {'Arrows (10)', 'Single Bomb', 'Bombs (3)', 'Bombs (10)', 'Nothing'}
