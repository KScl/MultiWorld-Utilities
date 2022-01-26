from collections import namedtuple
import logging

from BaseClasses import Region, RegionType, Location
from Shops import TakeAny, total_shop_slots, set_up_shops, shuffle_shops
from Bosses import place_bosses
from Dungeons import get_dungeon_item_pool
from EntranceShuffle import connect_entrance
from Fill import FillError, fill_restrictive, fast_fill
from Items import ItemFactory, GetBeemizerItem, item_name_groups
from Rules import forbid_items_for_player

import source.classes.constants as CONST

# This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
# Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

#easybaseitems = (['Rupees (300)'] * 5 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
#easyfirst15extra = ['Piece of Heart'] * 12 + ['Rupees (300)'] * 3
#easysecond15extra = ['Rupees (100)'] + ['Arrows (10)'] * 7 + ['Bombs (3)'] * 7
#easythird10extra = ['Bombs (3)'] * 7 + ['Rupee (1)', 'Rupees (50)', 'Bombs (10)']
#easyfourth5extra = ['Rupees (50)'] * 2 + ['Bombs (3)'] * 2 + ['Arrows (10)']
#easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 4 + ['Rupees (5)'] * 2
#normalbaseitems = (['Arrows (10)', 'Bombs (10)'] + ['Rupees (300)'] * 3 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
#normalfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Arrows (10)'] * 6 + ['Bombs (3)'] * 6
#normalsecond15extra = ['Bombs (3)'] * 10 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)']
#normalthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Arrows (10)', 'Rupee (1)', 'Rupees (5)']
#normalfourth5extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2 + ['Rupees (5)']
#normalfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2

Difficulty = namedtuple('Difficulty', [
    'bottles', 'bottle_count', 'progressive_bottle_limit', # 'same_bottle': if progressive_bottle_limit is 1
    'sworditems', 'shielditems', 'armoritems', 'bowitems', 'ngbowitems', 'magicitems',
    'progressive_sword_limit', 'progressive_shield_limit', 'progressive_armor_limit', 'progressive_bow_limit',
    'heartitems', 'heart_piece_limit', 'boss_heart_container_limit',
    'extraitems', 'legacybow', 'nglegacybow',
    'timedohko', 'timedother', 'universal_keys', 'universal_keys_drop',
])

Upgrades = namedtuple('Upgrades', ['progressive', 'standard'])

# No longer used
# total_items_to_place = 153

# 29 keys in vanilla
# 61 keys in key_drop_shuffle

# -----------------------------------------------------------------------------
# Always present items
# -----------------------------------------------------------------------------
medallion_items   = ['Bombos', 'Ether', 'Quake']
boomerang_items   = ['Blue Boomerang', 'Red Boomerang', 'Hookshot']
weapon_items      = ['Cane of Byrna', 'Cane of Somaria',  'Fire Rod', 'Hammer', 'Ice Rod']
legacy_pool_items = ['Magic Mirror', 'Moon Pearl'] # for insanity_legacy
other_items       = ['Book of Mudora',  'Bug Catching Net', 'Cape',  'Flippers', 'Flute', 'Lamp', 'Magic Powder', 'Mushroom', 'Pegasus Boots', 'Shovel']
always_items      = medallion_items + boomerang_items + weapon_items + legacy_pool_items + other_items

glove_upgrades = Upgrades(progressive=['Progressive Glove'] * 2, standard=['Power Glove', 'Titans Mitts'])
# -----------------------------------------------------------------------------
# Contents that are allowed to be in bottles when you first pick them up
# -----------------------------------------------------------------------------
expert_bottles = ['Bottle', 'Bottle (Bee)', 'Bottle (Good Bee)'] # Not used on its own
hard_bottles   = expert_bottles + ['Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)']
normal_bottles = hard_bottles + ['Bottle (Fairy)']
# -----------------------------------------------------------------------------
difficulties = {
    'easy': Difficulty(
        bottles=normal_bottles,
        bottle_count=8,
        progressive_bottle_limit=8,
        sworditems= Upgrades(progressive=['Progressive Sword'] * 8,   standard=['Master Sword', 'Tempered Sword', 'Golden Sword', 'Fighter Sword'] * 2),
        shielditems=Upgrades(progressive=['Progressive Shield'] * 6,  standard=['Blue Shield', 'Red Shield', 'Mirror Shield'] * 2),
        armoritems= Upgrades(progressive=['Progressive Mail'] * 4,    standard=['Blue Mail', 'Red Mail'] * 2),
        bowitems=   Upgrades(progressive=["Progressive Bow"] * 4,     standard=['Bow', 'Silver Bow'] * 2),
        ngbowitems= Upgrades(progressive=["Progressive Bow"] * 4,     standard=['Bow', 'Silver Bow'] * 2),
        magicitems= Upgrades(progressive=['Magic Upgrade (1/2)'] * 2, standard=['Magic Upgrade (1/2)', 'Magic Upgrade (1/4)']),
        progressive_sword_limit=8,
        progressive_shield_limit=6,
        progressive_armor_limit=4,
        progressive_bow_limit=4,
        heartitems=['Sanctuary Heart Container'] + ['Boss Heart Container'] * 16 + ['Piece of Heart'] * 24,
        boss_heart_container_limit=12,
        heart_piece_limit=12, # Enforced by the game (20 heart max)
        legacybow=  ['Bow', 'Silver Arrows'] * 2,
        nglegacybow=['Bow', 'Silver Arrows'] * 2,
        timedohko=  ['Green Clock'] * 25,
        timedother= ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        universal_keys=     ['Small Key (Universal)'] * 29,
        universal_keys_drop=['Small Key (Universal)'] * 61,
        extraitems=['Lamp']
    ),
    'normal': Difficulty(
        bottles=normal_bottles,
        bottle_count=4,
        progressive_bottle_limit=4,
        sworditems= Upgrades(progressive=['Progressive Sword'] * 4,   standard=['Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword']),
        shielditems=Upgrades(progressive=['Progressive Shield'] * 3,  standard=['Blue Shield', 'Red Shield', 'Mirror Shield']),
        armoritems= Upgrades(progressive=['Progressive Mail'] * 2,    standard=['Blue Mail', 'Red Mail']),
        bowitems=   Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow', 'Silver Bow']),
        ngbowitems= Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow', 'Silver Bow']),
        magicitems= ['Magic Upgrade (1/2)'],
        progressive_sword_limit=4,
        progressive_shield_limit=3,
        progressive_armor_limit=2,
        progressive_bow_limit=2,
        heartitems=['Sanctuary Heart Container'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24,
        boss_heart_container_limit=10,
        heart_piece_limit=24,
        legacybow=  ['Bow', 'Silver Arrows'],
        nglegacybow=['Bow', 'Silver Arrows'],
        timedohko=  ['Green Clock'] * 25,
        timedother= ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        universal_keys=     ['Small Key (Universal)'] * 20,
        universal_keys_drop=['Small Key (Universal)'] * 50,
        extraitems=['Single Arrow']
    ),
    'hard': Difficulty(
        bottles=hard_bottles,
        bottle_count=4,
        progressive_bottle_limit=4,
        sworditems= Upgrades(progressive=['Progressive Sword'] * 4,   standard=['Fighter Sword', 'Master Sword', 'Master Sword', 'Tempered Sword']),
        shielditems=Upgrades(progressive=['Progressive Shield'] * 3,  standard=['Blue Shield', 'Red Shield', 'Red Shield']),
        armoritems= Upgrades(progressive=['Progressive Mail'] * 2,    standard=['Blue Mail', 'Blue Mail']),
        bowitems=   Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow'] * 2),
        ngbowitems= Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow', 'Silver Bow']),
        magicitems= ['Magic Upgrade (1/2)'],
        progressive_sword_limit=3,
        progressive_shield_limit=2,
        progressive_armor_limit=1,
        progressive_bow_limit=1,
        heartitems=['Sanctuary Heart Container'] + ['Boss Heart Container'] * 8 + ['Piece of Heart'] * 20,
        boss_heart_container_limit=6,
        heart_piece_limit=16,
        legacybow=  ['Bow'],
        nglegacybow=['Bow', 'Silver Arrows'],
        timedohko=  ['Green Clock'] * 25,
        timedother= ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        universal_keys=     ['Small Key (Universal)'] * 14,
        universal_keys_drop=['Small Key (Universal)'] * 42,
        extraitems=['Single Arrow']
    ),
    'expert': Difficulty(
        bottles=hard_bottles,
        bottle_count=4,
        progressive_bottle_limit=4,
        sworditems= Upgrades(progressive=['Progressive Sword'] * 3,   standard=['Fighter Sword', 'Master Sword', 'Master Sword']),
        shielditems=Upgrades(progressive=['Progressive Shield'] * 2,  standard=['Blue Shield', 'Blue Shield']),
        armoritems= [], # Completely removed
        bowitems=   Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow'] * 2),
        ngbowitems= Upgrades(progressive=["Progressive Bow"] * 2,     standard=['Bow', 'Silver Bow']),
        magicitems= ['Magic Upgrade (1/2)'],
        progressive_sword_limit=2,
        progressive_shield_limit=1,
        progressive_armor_limit=0,
        progressive_bow_limit=1,
        heartitems=['Sanctuary Heart Container'] + ['Boss Heart Container'] * 4 + ['Piece of Heart'] * 12,
        boss_heart_container_limit=2,
        heart_piece_limit=8,
        legacybow=  ['Bow'],
        nglegacybow=['Bow', 'Silver Arrows'],
        timedohko=  ['Green Clock'] * 20 + ['Red Clock'] * 5,
        timedother= ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        universal_keys=     ['Small Key (Universal)'] * 14,
        universal_keys_drop=['Small Key (Universal)'] * 42,
        extraitems=['Single Arrow']
    ),
}

# Gets the "core" item pool, of every non-junk item in the seed.
# Returns a tuple of, in order:
#   - A list of items in the item pool
#   - A dictionary of required pre-placed locations and the items within them
#   - A list of items that the player must start with
def get_pool_core(world, player: int):
    shuffle = world.shuffle[player]
    difficulty = world.difficulty[player]
    goal = world.goal[player]
    mode = world.mode[player]
    swords = world.swords[player]
    retro = world.retro[player]
    logic = world.logic[player]

    # Return values
    pool = []
    placed_items = {}
    precollected_items = []

    diff = difficulties[difficulty]

    def place_item(loc, item):
        assert loc not in placed_items
        placed_items[loc] = item

    def get_possibly_progressive_items(pool, item_type):
        if type(pool) is Upgrades:
            return pool.progressive if world.want_progressives(player, item_type) else pool.standard
        return pool

    pool.extend(always_items)

    # insanity legacy shuffle doesn't have fake LW/DW logic so guaranteed Mirror and Moon Pearl at the start
    if shuffle == 'insanity_legacy':
        place_item("Link's House", legacy_pool_items[0])
        place_item("Sanctuary", legacy_pool_items[1])

    # provide boots to major glitch dependent seeds
    if logic in {'owglitches', 'nologic'} and world.glitch_boots[player]:
        precollected_items.append('Pegasus Boots')

    # expert+ difficulties produce the same contents for all bottles, since only one bottle is available
    # (not true anymore??)
    if diff.progressive_bottle_limit <= 1:
        pool.append([world.random.choice(diff.bottles)] * diff.bottle_count)
    else:
        [pool.append(world.random.choice(diff.bottles)) for _ in range(diff.bottle_count)]

    pool.extend(get_possibly_progressive_items(glove_upgrades, 'glove'))
    pool.extend(get_possibly_progressive_items(diff.shielditems, 'shield'))
    pool.extend(get_possibly_progressive_items(diff.armoritems, 'armor'))
    pool.extend(get_possibly_progressive_items(diff.magicitems, 'capacity'))

    if (swords == 'swordless' or logic == 'noglitches'): # Silvers required regardless of difficulty
        pool.extend(diff.nglegacybow if 'l' in world.progressive[player] else get_possibly_progressive_items(diff.ngbowitems))
    else:
        pool.extend(diff.legacybow if 'l' in world.progressive[player] else get_possibly_progressive_items(diff.bowitems))

    # -------------------------------------------------------------------------
    # Place weapons
    # -------------------------------------------------------------------------
    sword_pool = get_possibly_progressive_items(diff.sworditems, 'sword')
    if swords == 'swordless':
        sword_pool = []
    elif swords == 'vanilla':
        if 'Fighter Sword' in sword_pool:
            # Place Fighter Sword & Shield at Uncle (vanilla & pre-progressive VT behavior)
            place_item("Link's Uncle", 'Fighter Sword & Shield')
            sword_pool.remove('Fighter Sword') # Only one of them, for Expert has (had?) two

            # As we have the first shield now, remove it from the pool
            pool.remove('Blue Shield') if 'Blue Shield' in pool else pool.remove('Progressive Shield')
        else:
            place_item("Link's Uncle", sword_pool.pop())
 
        world.random.shuffle(sword_pool)
        place_item('Blacksmith', sword_pool.pop())
        place_item('Pyramid Fairy - Left', sword_pool.pop())
        place_item('Master Sword Pedestal', sword_pool.pop()) if goal != 'pedestal' else sword_pool.pop()
    elif swords == 'assured':
        precollected_items.append('Fighter Sword' if 'Fighter Sword' in sword_pool else 'Progressive Sword')

    pool.extend(sword_pool)
    # -------------------------------------------------------------------------

    # extraitems = total_items_to_place - len(pool) - len(placed_items)

    if world.timer[player] in ['timed', 'timed-countdown']:
        pool.extend(diff.timedother)
    elif world.timer[player] in ['timed-ohko']:
        pool.extend(diff.timedohko)

    if 'triforcehunt' in goal:
        pool.extend(["Treasure Hunt Item"] * world.triforce_pieces_available[player])

    if world.keyshuffle[player] == "universal":
        pool.extend(diff.universal_keys_drop if world.keydropshuffle[player] else diff.universal_keys)

        if world.doorShuffle[player] != 'vanilla':
            # Previous version of this code replaced some Rupees with universal keys
            # as it was done last; we moved this entire section up to place keys prior
            # to extra items, so we don't need to do that replacement
            pool.extend(['Small Key (Universal)'] * world.random.randint(1, 10))

        if mode == 'standard' and world.doorShuffle[player] == 'vanilla':
            key_locations = []
            current_locations = []
            if world.keydropshuffle[player]: # Need 4 (!) keys to finish escape
                key_locations = [
                    ["Link's House", 'Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Boomerang Guard Key Drop'],
                    ['Hyrule Castle - Map Chest', 'Hyrule Castle - Map Guard Key Drop'],
                    ["Hyrule Castle - Zelda's Chest", 'Hyrule Castle - Big Key Drop', 'Sewers - Dark Cross'],
                    ['Hyrule Castle - Key Rat Key Drop']
                ]
            else: # Need 1 key to finish escape
                key_locations = [
                    ['Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Map Chest', "Hyrule Castle - Zelda's Chest", 'Sewers - Dark Cross']
                ]
            for locations in key_locations:
                current_locations.extend(locations)
                place_key_here = world.random.choice(current_locations)
                current_locations.remove(place_key_here)
                place_item(place_key_here, item_to_place)
                pool.remove(item_to_place)

    # Remove requested items from pool
    # This can be dangerous if progression items are removed, use at your own risk
    for arg_remove in world.item_pool_remove[player]:
        try:
            if arg_remove in item_name_groups: # Allow choosing from an item group name
                choices = [i for i in pool if i in item_name_groups[arg_remove]]
                arg_remove = world.random.choice(choices)
            pool.remove(arg_remove)
        except Exception:
            pass # Silently fail

    # Add requested extra items to pool
    # This is generally safe no matter what you do, the new items are just treated as extras
    pool.extend(world.item_pool_extend[player])

    if retro:
        erase = {'Single Arrow', 'Arrows (10)', 'Arrow Upgrade (+5)', 'Arrow Upgrade (+10)'}
        pool = [item for item in pool if item not in erase]

    if goal == 'icerodhunt': # Everything precollected
        irh_pool = [item for item in pool if item == 'Ice Rod']
        irc_collect = [item for item in pool if item != 'Ice Rod']
        return (irh_pool, {}, irh_collect)

    [pool.remove(item) for item in precollected_items if item in pool]
    [pool.remove(item) for item in placed_items.values() if item in pool]
    return (pool, placed_items, precollected_items)


def generate_itempool(world, player: int):
    if world.difficulty[player] not in difficulties:
        raise NotImplementedError(f"Diffulty {world.difficulty[player]}")
    if world.goal[player] not in {'ganon', 'pedestal', 'dungeons', 'triforcehunt', 'localtriforcehunt', 'icerodhunt',
                                  'ganontriforcehunt', 'localganontriforcehunt', 'crystals', 'ganonpedestal', 'plando'}:
        raise NotImplementedError(f"Goal {world.goal[player]}")
    if world.mode[player] not in {'open', 'standard', 'inverted'}:
        raise NotImplementedError(f"Mode {world.mode[player]}")
    if world.timer[player] not in {False, 'none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'}:
        raise NotImplementedError(f"Timer {world.mode[player]}")

    # if the player can be in ohko at any point (even if not always),
    # we cannot rely on the player taking damage at any point
    if world.timer[player] in ['ohko', 'timed-ohko']:
        world.can_take_damage[player] = False

    # =========================================================================
    # set up Triforce placement for goals
    # -------------------------------------------------------------------------
    triforce_location = 'Ganon' # Kept as string for some special behavior later

    if world.goal[player] in ['plando']:
        # Do not place a goal.
        # One must be placed with the plandomizer or seed generation will fail.
        triforce_location = None
    elif world.goal[player] in ['triforcehunt', 'localtriforcehunt']:
        # Must turn in triforce pieces to win
        region = world.get_region('Light World', player)
        turnin_location = Location(player, "Murahdahla", parent=region)
        turnin_location.access_rule = lambda state: state.has_triforce_pieces(state.world.treasure_hunt_count[player], player)
        region.locations.append(turnin_location)
        world.dynamic_locations.append(turnin_location)
        world.clear_location_cache()

        triforce_location = turnin_location
    elif world.goal[player] in ['pedestal']:
        # Must pull pedestal to win
        triforce_location = world.get_location('Master Sword Pedestal', player)
    elif world.goal[player] in ['icerodhunt']:
        # Must kill Trinexx to win
        world.progression_balancing[player] = False
        triforce_location = world.get_location('Turtle Rock - Boss', player)
        # As this essentially makes one dungeon prize impossible to get, forbid pedestal or pyramid fairy from being required
        forbid_items_for_player(triforce_location, {'Red Pendant', 'Green Pendant', 'Blue Pendant', 'Crystal 5', 'Crystal 6'}, player)

        if world.boss_shuffle[player] != 'none':
            if 'turtle rock-' not in world.boss_shuffle[player]:
                world.boss_shuffle[player] = f'Turtle Rock-Trinexx;{world.boss_shuffle[player]}'
            else:
                logging.warning(f'Cannot guarantee that Trinexx is the boss of Turtle Rock for player {player}')
        # Note: icerodhunt precollects all items in get_pool_core except the ice rod

    # -------------------------------------------------------------------------
    if triforce_location is not None:
        if triforce_location == 'Ganon':
            triforce_location = world.get_location('Ganon', player)
        else: # Ensure Ganon has nothing so we don't try to place an item there (lol)
            ganon_location = world.get_location('Ganon', player)
            world.push_item(ganon_location, ItemFactory('Nothing', player), False)
            ganon_location.event = ganon_location.locked = True

        # now place the Triforce at the goal
        world.push_item(triforce_location, ItemFactory('Triforce', player), False)
        triforce_location.event = triforce_location.locked = True

    # Extra handling for treasure hunts
    treasure_hunt_goal = world.goal[player] in ['triforcehunt', 'localtriforcehunt', 'ganontriforcehunt', 'localganontriforcehunt']

    # =========================================================================
    # Set up other, non-goal events
    # -------------------------------------------------------------------------
    event_pairs = [
        ('Agahnim 1', 'Beat Agahnim 1'),
        ('Agahnim 2', 'Beat Agahnim 2'),
        ('Dark Blacksmith Ruins', 'Pick Up Purple Chest'),
        ('Frog', 'Get Frog'),
        ('Missing Smith', 'Return Smith'),
        ('Floodgate', 'Open Floodgate'),
        ('Trench 1 Switch', 'Trench 1 Filled'),
        ('Trench 2 Switch', 'Trench 2 Filled'),
        ('Swamp Drain', 'Drained Swamp'),
        ('Attic Cracked Floor', 'Shining Light'),
        ('Suspicious Maiden', 'Maiden Rescued'),
        ('Revealing Light', 'Maiden Unmasked'),
        ('Ice Block Drop', 'Convenient Block'),
        ('Flute Activation Spot', 'Activated Flute')
    ]

    if world.mode[player] == 'standard':
        event_pairs += [
            ('Zelda Pickup', 'Zelda Herself'),
            ('Zelda Drop Off', 'Zelda Delivered')
        ]

    for location_name, event_name in event_pairs:
        location = world.get_location(location_name, player)
        event = ItemFactory(event_name, player)
        world.push_item(location, event, False)
        location.event = location.locked = True
    # -------------------------------------------------------------------------

    # set up item pool
    # get_pool_core now handles progression items, things added by modes, etc.
    # and explicitly does not include junk items
    # junk items will be added to the pool at a later step
    pool, placed_items, precollected_items = get_pool_core(world, player)

    world.clock_mode[player] = {
        'timed': 'stopwatch',
        'timed-countdown': 'countdown',
        'timed-ohko': 'countdown-ohko',
        'display': 'stopwatch',
        'ohko': 'ohko'
    }.get(world.timer[player], False)

    if treasure_hunt_goal:
        treasure_hunt_count = world.triforce_pieces_required[player]
        treasure_hunt_icon = 'Triforce Piece' # TODO Possibly allow changing this
        pool = [(treasure_hunt_icon if item in 'Treasure Hunt Item' else item) for item in pool]
        world.treasure_hunt_count[player] = treasure_hunt_count % 999
        world.treasure_hunt_icon[player] = treasure_hunt_icon

    #if player in world.pool_adjustment.keys():
    #    amt = world.pool_adjustment[player]
    #    if amt < 0:
    #        for _ in range(amt, 0):
    #            toss_junk_item(pool)
    #    elif amt > 0:
    #        for _ in range(0, amt):
    #            pool.append('Rupees (20)' if world.goal[player] != 'icerodhunt' else 'Nothing')


    for item in precollected_items:
        world.push_precollected(ItemFactory(item, player))

    if world.mode[player] == 'standard' and not world.state.has_melee_weapon(player):
        if "Link's Uncle" not in placed_items:
            found_sword = False
            found_bow = False
            possible_weapons = []
            for item in pool:
                if item in ['Progressive Sword', 'Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword']:
                    if not found_sword and world.swords[player] != 'swordless':
                        found_sword = True
                        possible_weapons.append(item)
                if item in ['Progressive Bow', 'Bow'] and not found_bow:
                    found_bow = True
                    possible_weapons.append(item)
                if item in ['Hammer', 'Fire Rod', 'Cane of Somaria', 'Cane of Byrna']:
                    if item not in possible_weapons:
                        possible_weapons.append(item)
                if item in ['Bombs (10)']:
                    if item not in possible_weapons and world.doorShuffle[player] != 'crossed':
                        possible_weapons.append(item)
            starting_weapon = world.random.choice(possible_weapons)
            placed_items["Link's Uncle"] = starting_weapon
            pool.remove(starting_weapon)
        if placed_items["Link's Uncle"] in ['Bow', 'Progressive Bow', 'Bombs (10)', 'Cane of Somaria', 'Cane of Byrna'] and world.enemy_health[player] not in ['default', 'easy']:
            world.escape_assist[player].append('bombs')
        if world.doorShuffle[player] == 'crossed': # Crossed doors escape tends to be much more difficult
            if placed_items["Link's Uncle"] in ['Bow', 'Progressive Bow']:
                world.escape_assist[player].append('arrows')
            elif placed_items["Link's Uncle"] in ['Cane of Somaria', 'Cane of Byrna', 'Fire Rod']:
                world.escape_assist[player].append('magic')
            # Redundant as it's currently not allowed, but kept here just in case it is allowed later
            elif placed_items["Link's Uncle"] in ['Bombs (10)']:
                world.escape_assist[player].append('bombs')


    for (location, item) in placed_items.items():
        world.push_item(world.get_location(location, player), ItemFactory(item, player), False)
        world.get_location(location, player).event = True
        world.get_location(location, player).locked = True

    items = ItemFactory(pool, player)

    dungeon_items = [item for item in get_dungeon_item_pool(world) if item.player == player
                           and ((item.smallkey and world.keyshuffle[player])
                                or (item.bigkey and world.bigkeyshuffle[player])
                                or (item.map and world.mapshuffle[player])
                                or (item.compass and world.compassshuffle[player])
                                or world.goal[player] == 'icerodhunt')]

    if world.goal[player] == 'icerodhunt':
        for item in dungeon_items:
            world.itempool.append(ItemFactory(GetBeemizerItem(world, player, 'Nothing'), player))
            world.push_precollected(item)
    else:
        world.itempool.extend([item for item in dungeon_items])

    # logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
    # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
    # We mark one random heart container as an advancement item (or 4 heart pieces if none present, e.g. in expert mode)
    adv_hearts = [('Boss Heart Container', 1), ('Piece of Heart', 4), ('Sanctuary Heart Container', 1)]
    for (adv_item, adv_required) in adv_hearts:
        adv_items = [item for item in items if item.name == adv_item]
        if len(adv_items) >= adv_required:
            for i in range(adv_required):
                adv_items[i].advancement = True
            break

    progressionitems = []
    nonprogressionitems = []
    for item in items:
        if not item.is_nonprogression():
            progressionitems.append(item)
        else:
            nonprogressionitems.append(GetBeemizerItem(world, item.player, item))
    world.random.shuffle(nonprogressionitems)

    #if additional_triforce_pieces:
    #    if additional_triforce_pieces > len(nonprogressionitems):
    #        raise FillError(f"Not enough non-progression items to replace with Triforce pieces found for player "
    #                        f"{world.get_player_names(player)}.")
    #    progressionitems += [ItemFactory("Triforce Piece", player)] * additional_triforce_pieces
    #    nonprogressionitems.sort(key=lambda item: int("Heart" in item.name))  # try to keep hearts in the pool
    #    nonprogressionitems = nonprogressionitems[additional_triforce_pieces:]
    #    world.random.shuffle(nonprogressionitems)

    # shuffle medallions
    if world.required_medallions[player][0] == "random":
        mm_medallion = world.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        mm_medallion = world.required_medallions[player][0]
    if world.required_medallions[player][1] == "random":
        tr_medallion = world.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        tr_medallion = world.required_medallions[player][1]
    world.required_medallions[player] = (mm_medallion, tr_medallion)

    place_bosses(world, player)
    set_up_shops(world, player)

    if world.shop_shuffle[player]:
        shuffle_shops(world, nonprogressionitems, player)
    create_dynamic_shop_locations(world, player)

    world.itempool += progressionitems + nonprogressionitems

    if world.retro[player]:
        set_up_take_anys(world, player)  # depends on world.itempool to be set

    if world.keyshuffle[player] == "universal" and world.keydropshuffle[player]:
        world.itempool += [ItemFactory('Small Key (Universal)', player)] * 32


take_any_locations = {
    'Snitch Lady (East)', 'Snitch Lady (West)', 'Bush Covered House', 'Light World Bomb Hut',
    'Fortune Teller (Light)', 'Lake Hylia Fortune Teller', 'Lumberjack House', 'Bonk Fairy (Light)',
    'Bonk Fairy (Dark)', 'Lake Hylia Healer Fairy', 'Swamp Healer Fairy', 'Desert Healer Fairy',
    'Dark Lake Hylia Healer Fairy', 'Dark Lake Hylia Ledge Healer Fairy', 'Dark Desert Healer Fairy',
    'Dark Death Mountain Healer Fairy', 'Long Fairy Cave', 'Good Bee Cave', '20 Rupee Cave',
    'Kakariko Gamble Game', '50 Rupee Cave', 'Lost Woods Gamble', 'Hookshot Fairy',
    'Palace of Darkness Hint', 'East Dark World Hint', 'Archery Game', 'Dark Lake Hylia Ledge Hint',
    'Dark Lake Hylia Ledge Spike Cave', 'Fortune Teller (Dark)', 'Dark Sanctuary Hint', 'Dark Desert Hint'}

take_any_locations_inverted = list(take_any_locations - {"Dark Sanctuary Hint", "Archery Game"})
take_any_locations = list(take_any_locations)
# sets are sorted by the element's hash, python's hash is seeded at startup, resulting in different sorting each run
take_any_locations_inverted.sort()
take_any_locations.sort()


def set_up_take_anys(world, player):
    # these are references, do not modify these lists in-place
    if world.mode[player] == 'inverted':
        take_any_locs = take_any_locations_inverted
    else:
        take_any_locs = take_any_locations

    regions = world.random.sample(take_any_locs, 5)

    old_man_take_any = Region("Old Man Sword Cave", RegionType.Cave, 'the sword cave', player)
    world.regions.append(old_man_take_any)
    world.dynamic_regions.append(old_man_take_any)

    reg = regions.pop()
    entrance = world.get_region(reg, player).entrances[0]
    connect_entrance(world, entrance.name, old_man_take_any.name, player)
    entrance.target = 0x58
    old_man_take_any.shop = TakeAny(old_man_take_any, 0x0112, 0xE2, True, True, total_shop_slots)
    world.shops.append(old_man_take_any.shop)

    swords = [item for item in world.itempool if item.type == 'Sword' and item.player == player]
    if swords:
        sword = world.random.choice(swords)
        world.itempool.remove(sword)
        world.itempool.append(ItemFactory('Rupees (20)', player))
        old_man_take_any.shop.add_inventory(0, sword.name, 0, 0, create_location=True)
    else:
        old_man_take_any.shop.add_inventory(0, 'Rupees (300)', 0, 0)

    for num in range(4):
        take_any = Region("Take-Any #{}".format(num+1), RegionType.Cave, 'a cave of choice', player)
        world.regions.append(take_any)
        world.dynamic_regions.append(take_any)

        target, room_id = world.random.choice([(0x58, 0x0112), (0x60, 0x010F), (0x46, 0x011F)])
        reg = regions.pop()
        entrance = world.get_region(reg, player).entrances[0]
        connect_entrance(world, entrance.name, take_any.name, player)
        entrance.target = target
        take_any.shop = TakeAny(take_any, room_id, 0xE3, True, True, total_shop_slots + num + 1)
        world.shops.append(take_any.shop)
        take_any.shop.add_inventory(0, 'Blue Potion', 0, 0)
        take_any.shop.add_inventory(1, 'Boss Heart Container', 0, 0)

    world.initialize_regions()


def create_dynamic_shop_locations(world, player):
    for shop in world.shops:
        if shop.region.player == player:
            for i, item in enumerate(shop.inventory):
                if item is None:
                    continue
                if item['create_location']:
                    loc = Location(player, "{} Slot {}".format(shop.region.name, i + 1), parent=shop.region)
                    shop.region.locations.append(loc)
                    world.dynamic_locations.append(loc)

                    world.clear_location_cache()

                    world.push_item(loc, ItemFactory(item['item'], player), False)
                    loc.shop_slot = True
                    loc.event = True
                    loc.locked = True


def fill_prizes(world, attempts=15):
    all_state = world.get_all_state(keys=True)
    for player in range(1, world.players + 1):
        crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'], player)
        crystal_locations = [world.get_location('Turtle Rock - Prize', player), world.get_location('Eastern Palace - Prize', player), world.get_location('Desert Palace - Prize', player), world.get_location('Tower of Hera - Prize', player), world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player), world.get_location('Skull Woods - Prize', player), world.get_location('Swamp Palace - Prize', player), world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = list(unplaced_prizes)
                prize_locs = list(empty_crystal_locations)
                world.random.shuffle(prizepool)
                world.random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool, single_player_placement=True, lock=True)
            except FillError as e:
                logging.getLogger('').exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')
