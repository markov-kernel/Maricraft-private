"""Pre-defined Minecraft command buttons organized by category."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

# Maximum effect duration in game ticks (~55 days in-game)
# Used for "permanent" effects like GOD MODE that persist until cleared
INFINITE_EFFECT_TICKS = 99999


@dataclass
class CommandButton:
    """A single button that executes one or more commands."""
    name: str
    description: str
    commands: List[str]  # Java Edition commands
    color: str = "#3498DB"
    function_id: str = ""  # e.g., "buffs/god_mode" (Bedrock doesn't use namespace prefix)
    bedrock_commands: List[str] = None  # Bedrock Edition commands (optional)


@dataclass
class CommandCategory:
    """A category of related command buttons."""
    name: str
    buttons: List[CommandButton] = field(default_factory=list)


# === CATEGORY 1: BUFFS & EFFECTS ===
# Bedrock uses "/effect @s" instead of "/effect give @s"
BUFFS_EFFECTS = CommandCategory(
    name="Buffs & Effects",
    buttons=[
        CommandButton(
            name="Full Heal",
            description="Restore all health instantly",
            commands=["/effect give @s instant_health 1 255"],
            color="#FF6B6B",
            function_id="buffs/full_heal",
            bedrock_commands=["/effect @s instant_health 1 255"]
        ),
        CommandButton(
            name="Super Regen",
            description="Fast regeneration for 5 minutes",
            commands=["/effect give @s regeneration 300 2 true"],
            color="#4ECDC4",
            function_id="buffs/super_regen",
            bedrock_commands=["/effect @s regeneration 300 2 true"]
        ),
        CommandButton(
            name="Health Boost",
            description="Extra hearts for 10 minutes",
            commands=["/effect give @s health_boost 600 4 true"],
            color="#E74C3C",
            function_id="buffs/health_boost",
            bedrock_commands=["/effect @s health_boost 600 4 true"]
        ),
        CommandButton(
            name="Night Vision",
            description="See in the dark for 10 minutes",
            commands=["/effect give @s night_vision 600 0 true"],
            color="#9B59B6",
            function_id="buffs/night_vision",
            bedrock_commands=["/effect @s night_vision 600 0 true"]
        ),
        CommandButton(
            name="Speed Boost",
            description="Run super fast for 5 minutes",
            commands=["/effect give @s speed 300 2 true"],
            color="#3498DB",
            function_id="buffs/speed_boost",
            bedrock_commands=["/effect @s speed 300 2 true"]
        ),
        CommandButton(
            name="Jump Boost",
            description="Jump really high for 5 minutes",
            commands=["/effect give @s jump_boost 300 2 true"],
            color="#2ECC71",
            function_id="buffs/jump_boost",
            bedrock_commands=["/effect @s jump_boost 300 2 true"]
        ),
        CommandButton(
            name="Water Breathing",
            description="Breathe underwater for 10 minutes",
            commands=["/effect give @s water_breathing 600 0 true"],
            color="#00CED1",
            function_id="buffs/water_breathing",
            bedrock_commands=["/effect @s water_breathing 600 0 true"]
        ),
        CommandButton(
            name="Fire Resistance",
            description="Immune to fire for 10 minutes",
            commands=["/effect give @s fire_resistance 600 0 true"],
            color="#E67E22",
            function_id="buffs/fire_resistance",
            bedrock_commands=["/effect @s fire_resistance 600 0 true"]
        ),
        CommandButton(
            name="Slow Falling",
            description="Fall slowly for 5 minutes",
            commands=["/effect give @s slow_falling 300 0 true"],
            color="#F1C40F",
            function_id="buffs/slow_falling",
            bedrock_commands=["/effect @s slow_falling 300 0 true"]
        ),
        CommandButton(
            name="Invisibility",
            description="Become invisible for 5 minutes",
            commands=["/effect give @s invisibility 300 0 true"],
            color="#95A5A6",
            function_id="buffs/invisibility",
            bedrock_commands=["/effect @s invisibility 300 0 true"]
        ),
        CommandButton(
            name="Resistance",
            description="Take less damage for 5 minutes",
            commands=["/effect give @s resistance 300 2 true"],
            color="#7F8C8D",
            function_id="buffs/resistance",
            bedrock_commands=["/effect @s resistance 300 2 true"]
        ),
        CommandButton(
            name="Strength",
            description="Deal more damage for 5 minutes",
            commands=["/effect give @s strength 300 2 true"],
            color="#C0392B",
            function_id="buffs/strength",
            bedrock_commands=["/effect @s strength 300 2 true"]
        ),
        CommandButton(
            name="GOD MODE",
            description="All buffs: regen, resistance, strength, speed!",
            commands=[
                "/effect give @s regeneration 99999 4 true",
                "/effect give @s resistance 99999 4 true",
                "/effect give @s strength 99999 2 true",
                "/effect give @s speed 99999 1 true",
                "/effect give @s fire_resistance 99999 0 true",
                "/effect give @s night_vision 99999 0 true",
                "/effect give @s health_boost 99999 4 true",
            ],
            color="#FFD700",
            function_id="buffs/god_mode",
            bedrock_commands=[
                "/effect @s regeneration 99999 4 true",
                "/effect @s resistance 99999 4 true",
                "/effect @s strength 99999 2 true",
                "/effect @s speed 99999 1 true",
                "/effect @s fire_resistance 99999 0 true",
                "/effect @s night_vision 99999 0 true",
                "/effect @s health_boost 99999 4 true",
            ]
        ),
        CommandButton(
            name="Clear Effects",
            description="Remove all active effects",
            commands=["/effect clear @s"],
            color="#BDC3C7",
            function_id="buffs/clear_effects",
            bedrock_commands=["/effect @s clear"]
        ),
        CommandButton(
            name="Saturation",
            description="Never get hungry for 10 minutes",
            commands=["/effect give @s saturation 600 0 true"],
            color="#F39C12",
            function_id="buffs/saturation",
            bedrock_commands=["/effect @s saturation 600 0 true"]
        ),
        CommandButton(
            name="Haste",
            description="Mine faster for 5 minutes",
            commands=["/effect give @s haste 300 2 true"],
            color="#1ABC9C",
            function_id="buffs/haste",
            bedrock_commands=["/effect @s haste 300 2 true"]
        ),
    ]
)


# === CATEGORY 2: GEAR & ITEMS ===
# Bedrock can't use NBT in /give, must use /enchant after giving item
GEAR_ITEMS = CommandCategory(
    name="Gear & Items",
    buttons=[
        CommandButton(
            name="Diamond Armor",
            description="Full diamond armor set",
            commands=[
                "/give @s diamond_helmet 1",
                "/give @s diamond_chestplate 1",
                "/give @s diamond_leggings 1",
                "/give @s diamond_boots 1",
            ],
            color="#00BFFF",
            function_id="gear/diamond_armor"
            # Same for Bedrock - no enchantments needed
        ),
        CommandButton(
            name="Netherite Armor",
            description="Full netherite armor set",
            commands=[
                "/give @s netherite_helmet 1",
                "/give @s netherite_chestplate 1",
                "/give @s netherite_leggings 1",
                "/give @s netherite_boots 1",
            ],
            color="#4A4A4A",
            function_id="gear/netherite_armor"
            # Same for Bedrock - no enchantments needed
        ),
        CommandButton(
            name="Super Sword",
            description="Netherite sword with best enchants",
            commands=[
                '/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2,looting:3,unbreaking:3,mending:1}}] 1'
            ],
            color="#8E44AD",
            function_id="gear/super_sword",
            bedrock_commands=[
                "/give @s netherite_sword 1",
                "/enchant @s sharpness 5",
                "/enchant @s fire_aspect 2",
                "/enchant @s looting 3",
                "/enchant @s unbreaking 3",
                "/enchant @s mending 1",
            ]
        ),
        CommandButton(
            name="Super Bow",
            description="Bow with power 5 and infinity",
            commands=[
                '/give @s bow[enchantments={levels:{power:5,flame:1,infinity:1,unbreaking:3}}] 1',
                "/give @s arrow 64",
            ],
            color="#D35400",
            function_id="gear/super_bow",
            bedrock_commands=[
                "/give @s bow 1",
                "/enchant @s power 5",
                "/enchant @s flame 1",
                "/enchant @s infinity 1",
                "/enchant @s unbreaking 3",
                "/give @s arrow 64",
            ]
        ),
        CommandButton(
            name="Super Pickaxe",
            description="Netherite pickaxe for fast mining",
            commands=[
                '/give @s netherite_pickaxe[enchantments={levels:{efficiency:5,fortune:3,unbreaking:3,mending:1}}] 1'
            ],
            color="#1ABC9C",
            function_id="gear/super_pickaxe",
            bedrock_commands=[
                "/give @s netherite_pickaxe 1",
                "/enchant @s efficiency 5",
                "/enchant @s fortune 3",
                "/enchant @s unbreaking 3",
                "/enchant @s mending 1",
            ]
        ),
        CommandButton(
            name="Super Axe",
            description="Netherite axe with sharpness",
            commands=[
                '/give @s netherite_axe[enchantments={levels:{sharpness:5,efficiency:5,unbreaking:3,mending:1}}] 1'
            ],
            color="#795548",
            function_id="gear/super_axe",
            bedrock_commands=[
                "/give @s netherite_axe 1",
                "/enchant @s sharpness 5",
                "/enchant @s efficiency 5",
                "/enchant @s unbreaking 3",
                "/enchant @s mending 1",
            ]
        ),
        CommandButton(
            name="Elytra + Rockets",
            description="Wings to fly plus firework rockets",
            commands=[
                '/give @s elytra[unbreakable={}] 1',
                "/give @s firework_rocket 64",
            ],
            color="#9B59B6",
            function_id="gear/elytra_rockets",
            bedrock_commands=[
                "/give @s elytra 1",
                "/enchant @s unbreaking 3",
                "/enchant @s mending 1",
                "/give @s firework_rocket 64",
            ]
        ),
        CommandButton(
            name="Trident",
            description="Trident with loyalty and channeling",
            commands=[
                '/give @s trident[enchantments={levels:{loyalty:3,channeling:1,impaling:5,unbreaking:3}}] 1'
            ],
            color="#3498DB",
            function_id="gear/trident",
            bedrock_commands=[
                "/give @s trident 1",
                "/enchant @s loyalty 3",
                "/enchant @s channeling 1",
                "/enchant @s impaling 5",
                "/enchant @s unbreaking 3",
            ]
        ),
        CommandButton(
            name="Shield",
            description="Unbreakable shield",
            commands=['/give @s shield[unbreakable={}] 1'],
            color="#7F8C8D",
            function_id="gear/shield",
            bedrock_commands=[
                "/give @s shield 1",
                "/enchant @s unbreaking 3",
                "/enchant @s mending 1",
            ]
        ),
        CommandButton(
            name="Golden Apples",
            description="Stack of 64 golden apples",
            commands=["/give @s golden_apple 64"],
            color="#F1C40F",
            function_id="gear/golden_apples"
            # Same for Bedrock
        ),
        CommandButton(
            name="Enchanted Apples",
            description="Stack of enchanted golden apples (Notch apples)",
            commands=["/give @s enchanted_golden_apple 64"],
            color="#FFD700",
            function_id="gear/enchanted_apples"
            # Same for Bedrock
        ),
        CommandButton(
            name="Ender Pearls",
            description="Stack of 16 ender pearls",
            commands=["/give @s ender_pearl 16"],
            color="#2C3E50",
            function_id="gear/ender_pearls"
            # Same for Bedrock
        ),
        CommandButton(
            name="Totem of Undying",
            description="Saves you from death",
            commands=["/give @s totem_of_undying 1"],
            color="#27AE60",
            function_id="gear/totem"
            # Same for Bedrock
        ),
        CommandButton(
            name="Crossbow",
            description="Quick charge crossbow with multishot",
            commands=[
                '/give @s crossbow[enchantments={levels:{quick_charge:3,multishot:1,unbreaking:3}}] 1'
            ],
            color="#6C5B7B",
            function_id="gear/crossbow",
            bedrock_commands=[
                "/give @s crossbow 1",
                "/enchant @s quick_charge 3",
                "/enchant @s multishot 1",
                "/enchant @s unbreaking 3",
            ]
        ),
        CommandButton(
            name="Full Tool Set",
            description="All netherite tools with enchants",
            commands=[
                '/give @s netherite_pickaxe[enchantments={levels:{efficiency:5,fortune:3,unbreaking:3}}] 1',
                '/give @s netherite_shovel[enchantments={levels:{efficiency:5,unbreaking:3}}] 1',
                '/give @s netherite_axe[enchantments={levels:{efficiency:5,unbreaking:3}}] 1',
                '/give @s netherite_hoe[enchantments={levels:{efficiency:5,unbreaking:3}}] 1',
            ],
            color="#34495E",
            function_id="gear/full_tool_set",
            bedrock_commands=[
                "/give @s netherite_pickaxe 1",
                "/enchant @s efficiency 5",
                "/enchant @s fortune 3",
                "/enchant @s unbreaking 3",
                "/give @s netherite_shovel 1",
                "/enchant @s efficiency 5",
                "/enchant @s unbreaking 3",
                "/give @s netherite_axe 1",
                "/enchant @s efficiency 5",
                "/enchant @s unbreaking 3",
                "/give @s netherite_hoe 1",
                "/enchant @s efficiency 5",
                "/enchant @s unbreaking 3",
            ]
        ),
        CommandButton(
            name="Steak x64",
            description="Stack of cooked steak",
            commands=["/give @s cooked_beef 64"],
            color="#A93226",
            function_id="gear/steak"
            # Same for Bedrock
        ),
    ]
)


# === CATEGORY 3: TELEPORT & LOCATE ===
# Bedrock uses different /execute syntax and /locate with different structure IDs
TELEPORT_LOCATE = CommandCategory(
    name="Teleport & Locate",
    buttons=[
        CommandButton(
            name="Find Village",
            description="Locate nearest village",
            commands=["/locate structure village"],
            color="#8D6E63",
            function_id="teleport/find_village",
            bedrock_commands=["/locate structure village"]
        ),
        CommandButton(
            name="Find Stronghold",
            description="Locate the End portal",
            commands=["/locate structure stronghold"],
            color="#607D8B",
            function_id="teleport/find_stronghold",
            bedrock_commands=["/locate structure stronghold"]
        ),
        CommandButton(
            name="Find Mansion",
            description="Locate woodland mansion",
            commands=["/locate structure mansion"],
            color="#795548",
            function_id="teleport/find_mansion",
            bedrock_commands=["/locate structure mansion"]
        ),
        CommandButton(
            name="Find Monument",
            description="Locate ocean monument",
            commands=["/locate structure monument"],
            color="#00ACC1",
            function_id="teleport/find_monument",
            bedrock_commands=["/locate structure monument"]
        ),
        CommandButton(
            name="Find Fortress",
            description="Locate nether fortress (use in Nether)",
            commands=["/locate structure fortress"],
            color="#B71C1C",
            function_id="teleport/find_fortress",
            bedrock_commands=["/locate structure fortress"]
        ),
        CommandButton(
            name="Find Bastion",
            description="Locate bastion remnant (use in Nether)",
            commands=["/locate structure bastion_remnant"],
            color="#424242",
            function_id="teleport/find_bastion",
            bedrock_commands=["/locate structure bastion_remnant"]
        ),
        CommandButton(
            name="Find Temple",
            description="Locate desert or jungle temple",
            commands=["/locate structure desert_pyramid"],
            color="#FFB74D",
            function_id="teleport/find_temple",
            bedrock_commands=["/locate structure desert_pyramid"]
        ),
        CommandButton(
            name="Find Mineshaft",
            description="Locate abandoned mineshaft",
            commands=["/locate structure mineshaft"],
            color="#8D6E63",
            function_id="teleport/find_mineshaft",
            bedrock_commands=["/locate structure mineshaft"]
        ),
        CommandButton(
            name="TP to Spawn",
            description="Teleport to world spawn (0, ?, 0)",
            commands=["/tp @s 0 100 0"],
            color="#4CAF50",
            function_id="teleport/tp_spawn"
            # Same for Bedrock
        ),
        CommandButton(
            name="TP Up 50",
            description="Teleport 50 blocks up",
            commands=["/tp @s ~ ~50 ~"],
            color="#03A9F4",
            function_id="teleport/tp_up_50"
            # Same for Bedrock
        ),
        CommandButton(
            name="TP Forward 100",
            description="Teleport 100 blocks forward (where you're looking)",
            commands=["/execute at @s run tp @s ^0 ^0 ^100"],
            color="#9C27B0",
            function_id="teleport/tp_forward_100",
            bedrock_commands=["/execute @s ~~~ tp @s ^0 ^0 ^100"]
        ),
        CommandButton(
            name="TP Back 75",
            description="Teleport 75 blocks backward",
            commands=["/execute at @s run tp @s ^0 ^0 ^-75"],
            color="#FF5722",
            function_id="teleport/tp_back_75",
            bedrock_commands=["/execute @s ~~~ tp @s ^0 ^0 ^-75"]
        ),
        CommandButton(
            name="TP to Surface",
            description="Teleport to highest block at your position",
            commands=["/tp @s ~ 320 ~", "/effect give @s slow_falling 10 0 true"],
            color="#81C784",
            function_id="teleport/tp_surface",
            bedrock_commands=["/tp @s ~ 320 ~", "/effect @s slow_falling 10 0 true"]
        ),
        CommandButton(
            name="Find End City",
            description="Locate end city (use in The End)",
            commands=["/locate structure end_city"],
            color="#CE93D8",
            function_id="teleport/find_end_city",
            bedrock_commands=["/locate structure end_city"]
        ),
        CommandButton(
            name="Find Trail Ruins",
            description="Locate trail ruins",
            commands=["/locate structure trail_ruins"],
            color="#BCAAA4",
            function_id="teleport/find_trail_ruins",
            bedrock_commands=["/locate structure trail_ruins"]
        ),
        CommandButton(
            name="Find Ancient City",
            description="Locate ancient city (deep underground)",
            commands=["/locate structure ancient_city"],
            color="#455A64",
            function_id="teleport/find_ancient_city",
            bedrock_commands=["/locate structure ancient_city"]
        ),
    ]
)


# === CATEGORY 4: WORLD CONTROL ===
WORLD_CONTROL = CommandCategory(
    name="World Control",
    buttons=[
        CommandButton(
            name="Set Day",
            description="Change time to morning",
            commands=["/time set day"],
            color="#FFD54F",
            function_id="world/set_day"
        ),
        CommandButton(
            name="Set Noon",
            description="Change time to noon",
            commands=["/time set noon"],
            color="#FFEB3B",
            function_id="world/set_noon"
        ),
        CommandButton(
            name="Set Night",
            description="Change time to night",
            commands=["/time set night"],
            color="#37474F",
            function_id="world/set_night"
        ),
        CommandButton(
            name="Clear Weather",
            description="Stop rain and thunder",
            commands=["/weather clear"],
            color="#81D4FA",
            function_id="world/clear_weather"
        ),
        CommandButton(
            name="Make Rain",
            description="Start raining",
            commands=["/weather rain"],
            color="#78909C",
            function_id="world/make_rain"
        ),
        CommandButton(
            name="Thunderstorm",
            description="Start a thunderstorm",
            commands=["/weather thunder"],
            color="#455A64",
            function_id="world/thunderstorm"
        ),
        CommandButton(
            name="Peaceful",
            description="No monsters spawn",
            commands=["/difficulty peaceful"],
            color="#A5D6A7",
            function_id="world/peaceful"
        ),
        CommandButton(
            name="Easy Mode",
            description="Monsters do less damage",
            commands=["/difficulty easy"],
            color="#C5E1A5",
            function_id="world/easy_mode"
        ),
        CommandButton(
            name="Normal Mode",
            description="Normal monster difficulty",
            commands=["/difficulty normal"],
            color="#FFCC80",
            function_id="world/normal_mode"
        ),
        CommandButton(
            name="Hard Mode",
            description="Monsters do more damage",
            commands=["/difficulty hard"],
            color="#EF9A9A",
            function_id="world/hard_mode"
        ),
        CommandButton(
            name="Creative Mode",
            description="Fly and infinite items",
            commands=["/gamemode creative"],
            color="#CE93D8",
            function_id="world/creative_mode"
        ),
        CommandButton(
            name="Survival Mode",
            description="Normal survival gameplay",
            commands=["/gamemode survival"],
            color="#90CAF9",
            function_id="world/survival_mode"
        ),
        CommandButton(
            name="Spectator Mode",
            description="Fly through blocks invisibly",
            commands=["/gamemode spectator"],
            color="#B0BEC5",
            function_id="world/spectator_mode"
        ),
        CommandButton(
            name="Keep Inventory",
            description="Keep items when you die",
            commands=["/gamerule keepInventory true"],
            color="#80CBC4",
            function_id="world/keep_inventory"
        ),
        CommandButton(
            name="Kill Hostiles",
            description="Remove hostile mobs nearby",
            commands=["/kill @e[type=#minecraft:raiders,distance=..100]"],
            color="#E57373",
            function_id="world/kill_hostiles",
            # Bedrock: kill common hostile mobs individually (no entity tags)
            bedrock_commands=[
                "/kill @e[type=zombie,r=100]",
                "/kill @e[type=skeleton,r=100]",
                "/kill @e[type=creeper,r=100]",
                "/kill @e[type=spider,r=100]",
                "/kill @e[type=enderman,r=100]",
                "/kill @e[type=witch,r=100]",
            ]
        ),
        CommandButton(
            name="Freeze Time",
            description="Stop the day/night cycle",
            commands=["/gamerule doDaylightCycle false"],
            color="#B39DDB",
            function_id="world/freeze_time"
        ),
    ]
)


# === CATEGORY 5: BUILDING & CREATION ===
BUILDING_CREATION = CommandCategory(
    name="Building & Creation",
    buttons=[
        CommandButton(
            name="Clear Area 10x10",
            description="Remove all blocks in a 10x10x10 cube around you",
            commands=["/fill ~-5 ~ ~-5 ~5 ~10 ~5 air"],
            color="#8BC34A",
            function_id="building/clear_area"
            # Same for Bedrock
        ),
        CommandButton(
            name="Glass Platform",
            description="Create a glass floor beneath you",
            commands=["/fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 glass"],
            color="#81D4FA",
            function_id="building/glass_platform"
            # Same for Bedrock
        ),
        CommandButton(
            name="Stone House",
            description="Build a small stone house instantly",
            commands=[
                "/fill ~2 ~ ~2 ~8 ~4 ~8 stone hollow",
                "/fill ~2 ~5 ~2 ~8 ~5 ~8 stone_bricks",
                "/setblock ~5 ~ ~2 oak_door[half=lower]",
                "/setblock ~5 ~1 ~2 oak_door[half=upper]",
                "/fill ~3 ~1 ~8 ~4 ~2 ~8 glass",
                "/fill ~6 ~1 ~8 ~7 ~2 ~8 glass",
            ],
            color="#9E9E9E",
            function_id="building/stone_house",
            bedrock_commands=[
                "/fill ~2 ~ ~2 ~8 ~4 ~8 stone 0 hollow",
                "/fill ~2 ~5 ~2 ~8 ~5 ~8 stonebrick",
                "/setblock ~5 ~ ~2 wooden_door",
                "/fill ~3 ~1 ~8 ~4 ~2 ~8 glass",
                "/fill ~6 ~1 ~8 ~7 ~2 ~8 glass",
            ]
        ),
        CommandButton(
            name="Wood Bridge 20",
            description="Build a wooden bridge in front of you (20 blocks)",
            commands=["/fill ^-1 ^-1 ^1 ^1 ^-1 ^20 oak_planks"],
            color="#8D6E63",
            function_id="building/wood_bridge",
            bedrock_commands=["/fill ^-1 ^-1 ^1 ^1 ^-1 ^20 planks"]
        ),
        CommandButton(
            name="Light Up Area",
            description="Place sea lanterns in a grid pattern",
            commands=[
                "/setblock ~-4 ~-1 ~-4 sea_lantern",
                "/setblock ~4 ~-1 ~-4 sea_lantern",
                "/setblock ~-4 ~-1 ~4 sea_lantern",
                "/setblock ~4 ~-1 ~4 sea_lantern",
                "/setblock ~ ~-1 ~ sea_lantern",
            ],
            color="#FFEB3B",
            function_id="building/light_up"
            # Same for Bedrock
        ),
        CommandButton(
            name="Water Pool",
            description="Create a small water pool",
            commands=[
                "/fill ~-3 ~-2 ~-3 ~3 ~-2 ~3 stone",
                "/fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 water",
            ],
            color="#2196F3",
            function_id="building/water_pool"
            # Same for Bedrock
        ),
        CommandButton(
            name="Lava Moat",
            description="Dig a moat and fill with lava (careful!)",
            commands=[
                "/fill ~-6 ~-2 ~-6 ~6 ~-1 ~-5 lava",
                "/fill ~-6 ~-2 ~5 ~6 ~-1 ~6 lava",
                "/fill ~-6 ~-2 ~-4 ~-5 ~-1 ~4 lava",
                "/fill ~5 ~-2 ~-4 ~6 ~-1 ~4 lava",
            ],
            color="#FF5722",
            function_id="building/lava_moat"
            # Same for Bedrock
        ),
        CommandButton(
            name="Remove Water",
            description="Drain all water in a 20-block radius",
            commands=["/fill ~-10 ~-5 ~-10 ~10 ~5 ~10 air replace water"],
            color="#4FC3F7",
            function_id="building/remove_water"
            # Same for Bedrock
        ),
        # === ELABORATE STRUCTURES ===
        CommandButton(
            name="Medieval Castle",
            description="Build an epic castle with towers, walls, and moat!",
            commands=["/say Building castle..."],  # Java fallback
            color="#607D8B",
            function_id="building/medieval_castle"
        ),
        CommandButton(
            name="Wizard Tower",
            description="Build a mystical wizard tower with enchanting room!",
            commands=["/say Building wizard tower..."],  # Java fallback
            color="#7B1FA2",
            function_id="building/wizard_tower"
        ),
        CommandButton(
            name="Pirate Ship",
            description="Build a full pirate ship with sails and treasure!",
            commands=["/say Building pirate ship..."],  # Java fallback
            color="#5D4037",
            function_id="building/pirate_ship"
        ),
        CommandButton(
            name="Underwater Dome",
            description="Build a glass dome base - perfect underwater!",
            commands=["/say Building underwater dome..."],  # Java fallback
            color="#00BCD4",
            function_id="building/underwater_dome"
        ),
        CommandButton(
            name="Pyramid",
            description="Build an ancient pyramid with hidden treasure chamber!",
            commands=["/say Building pyramid..."],  # Java fallback
            color="#FFC107",
            function_id="building/pyramid"
        ),
        CommandButton(
            name="Dragon Nest",
            description="Build an epic dragon nest with dragon egg and gold!",
            commands=["/say Building dragon nest..."],  # Java fallback
            color="#4A148C",
            function_id="building/dragon_nest"
        ),
    ]
)


# === CATEGORY 6: FRIENDLY MOBS ===
FRIENDLY_MOBS = CommandCategory(
    name="Friendly Mobs",
    buttons=[
        CommandButton(
            name="Wolf Pack",
            description="Spawn 5 tamed wolves (Java only - Bedrock: bring bones!)",
            commands=[
                "/summon wolf ~ ~ ~ {Tame:1b,CollarColor:14}",
                "/summon wolf ~1 ~ ~ {Tame:1b,CollarColor:11}",
                "/summon wolf ~-1 ~ ~ {Tame:1b,CollarColor:1}",
                "/summon wolf ~ ~ ~1 {Tame:1b,CollarColor:4}",
                "/summon wolf ~ ~ ~-1 {Tame:1b,CollarColor:5}",
            ],
            color="#A1887F",
            function_id="mobs/wolf_pack",
            bedrock_commands=[
                "/summon wolf ~ ~ ~",
                "/summon wolf ~1 ~ ~",
                "/summon wolf ~-1 ~ ~",
                "/summon wolf ~ ~ ~1",
                "/summon wolf ~ ~ ~-1",
                "/give @s bone 10",
            ]
        ),
        CommandButton(
            name="Cat Friend",
            description="Spawn a tamed cat (Java only - Bedrock: bring fish!)",
            commands=['/summon cat ~ ~ ~ {Tame:1b,variant:"minecraft:black"}'],
            color="#FF8A65",
            function_id="mobs/cat_friend",
            bedrock_commands=[
                "/summon cat ~ ~ ~",
                "/give @s fish 5",
            ]
        ),
        CommandButton(
            name="Horse + Saddle",
            description="Spawn a saddled horse ready to ride",
            commands=['/summon horse ~ ~ ~ {Tame:1b,SaddleItem:{id:"minecraft:saddle",count:1}}'],
            color="#795548",
            function_id="mobs/horse_saddle",
            bedrock_commands=[
                "/summon horse ~ ~ ~ minecraft:ageable_grow_up",
                "/give @s saddle 1",
            ]
        ),
        CommandButton(
            name="Parrot Party",
            description="Spawn 3 colorful parrots",
            commands=[
                "/summon parrot ~ ~ ~ {Variant:0}",
                "/summon parrot ~1 ~ ~ {Variant:1}",
                "/summon parrot ~-1 ~ ~ {Variant:2}",
            ],
            color="#4CAF50",
            function_id="mobs/parrot_party",
            bedrock_commands=[
                "/summon parrot ~ ~ ~",
                "/summon parrot ~1 ~ ~",
                "/summon parrot ~-1 ~ ~",
            ]
        ),
        CommandButton(
            name="Iron Golem",
            description="Spawn a protective iron golem",
            commands=["/summon iron_golem ~ ~ ~"],
            color="#78909C",
            function_id="mobs/iron_golem"
            # Same for Bedrock
        ),
        CommandButton(
            name="Snow Golem",
            description="Spawn a snow golem friend",
            commands=["/summon snow_golem ~ ~ ~"],
            color="#ECEFF1",
            function_id="mobs/snow_golem"
            # Same for Bedrock
        ),
        CommandButton(
            name="Dolphin",
            description="Spawn a friendly dolphin (needs water!)",
            commands=["/summon dolphin ~ ~ ~"],
            color="#00BCD4",
            function_id="mobs/dolphin"
            # Same for Bedrock
        ),
        CommandButton(
            name="Bee Hive",
            description="Spawn bees with a bee nest",
            commands=[
                "/setblock ~ ~2 ~ bee_nest",
                "/summon bee ~ ~3 ~",
                "/summon bee ~1 ~3 ~",
                "/summon bee ~-1 ~3 ~",
            ],
            color="#FFC107",
            function_id="mobs/bee_hive"
            # Same for Bedrock
        ),
    ]
)


# === CATEGORY 7: FUN & COSMETIC ===
FUN_COSMETIC = CommandCategory(
    name="Fun & Cosmetic",
    buttons=[
        CommandButton(
            name="Firework Show",
            description="Launch colorful fireworks all around",
            commands=[
                '/summon firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{explosions:[{shape:"large_ball",colors:[I;16711680],has_trail:1b}],flight_duration:1b}}}}',
                '/summon firework_rocket ~3 ~1 ~ {LifeTime:25,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{explosions:[{shape:"star",colors:[I;65280],has_trail:1b}],flight_duration:1b}}}}',
                '/summon firework_rocket ~-3 ~1 ~ {LifeTime:30,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{explosions:[{shape:"burst",colors:[I;255],has_trail:1b}],flight_duration:1b}}}}',
                '/summon firework_rocket ~ ~1 ~3 {LifeTime:35,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{explosions:[{shape:"large_ball",colors:[I;16776960],has_twinkle:1b}],flight_duration:1b}}}}',
            ],
            color="#FF4081",
            function_id="fun/firework_show",
            bedrock_commands=[
                "/summon fireworks_rocket ~ ~1 ~",
                "/summon fireworks_rocket ~3 ~1 ~",
                "/summon fireworks_rocket ~-3 ~1 ~",
                "/summon fireworks_rocket ~ ~1 ~3",
            ]
        ),
        CommandButton(
            name="Lightning Strike",
            description="Strike lightning where you stand!",
            commands=["/summon lightning_bolt ~ ~ ~"],
            color="#FFC107",
            function_id="fun/lightning_strike"
            # Same for Bedrock
        ),
        CommandButton(
            name="Giant Jump",
            description="Launch yourself super high into the air!",
            commands=[
                "/effect give @s levitation 2 50 true",
                "/effect give @s slow_falling 30 0 true",
            ],
            color="#7C4DFF",
            function_id="fun/giant_jump",
            bedrock_commands=[
                "/effect @s levitation 2 50 true",
                "/effect @s slow_falling 30 0 true",
            ]
        ),
        CommandButton(
            name="Disco Lights",
            description="Spawn colorful particle effects",
            commands=[
                "/particle dust{color:[1.0,0.0,0.0],scale:2} ~ ~2 ~ 3 3 3 0 50",
                "/particle dust{color:[0.0,1.0,0.0],scale:2} ~ ~2 ~ 3 3 3 0 50",
                "/particle dust{color:[0.0,0.0,1.0],scale:2} ~ ~2 ~ 3 3 3 0 50",
                "/particle dust{color:[1.0,1.0,0.0],scale:2} ~ ~2 ~ 3 3 3 0 50",
            ],
            color="#E040FB",
            function_id="fun/disco_lights",
            bedrock_commands=[
                "/particle minecraft:balloon_gas_particle ~ ~2 ~",
                "/particle minecraft:falling_dust ~ ~2 ~",
            ]
        ),
        CommandButton(
            name="Confetti",
            description="Celebrate with confetti particles!",
            commands=[
                "/particle totem_of_undying ~ ~1 ~ 1 1 1 0.5 100",
            ],
            color="#FF80AB",
            function_id="fun/confetti",
            bedrock_commands=["/particle minecraft:totem_particle ~ ~1 ~"]
        ),
        CommandButton(
            name="Safe Fire",
            description="Set yourself on fire (with fire resistance!)",
            commands=[
                "/effect give @s fire_resistance 60 0 true",
                "/effect give @s regeneration 60 1 true",
                "/summon armor_stand ~ ~ ~ {Invisible:1b,Fire:100,NoGravity:1b,Small:1b,Marker:1b}",
            ],
            color="#FF6E40",
            function_id="fun/safe_fire",
            bedrock_commands=[
                "/effect @s fire_resistance 60 0 true",
                "/effect @s regeneration 60 1 true",
            ]
        ),
        CommandButton(
            name="Rainbow Sheep",
            description="Spawn a magical color-changing sheep!",
            commands=['/summon sheep ~ ~ ~ {CustomName:\'"jeb_"\'}'],
            color="#9C27B0",
            function_id="fun/rainbow_sheep",
            bedrock_commands=['/summon sheep ~ ~ ~ minecraft:entity_born "jeb_"']
        ),
        CommandButton(
            name="Flower Circle",
            description="Create a circle of flowers around you",
            commands=[
                "/setblock ~3 ~ ~ poppy",
                "/setblock ~-3 ~ ~ dandelion",
                "/setblock ~ ~ ~3 blue_orchid",
                "/setblock ~ ~ ~-3 allium",
                "/setblock ~2 ~ ~2 azure_bluet",
                "/setblock ~-2 ~ ~2 red_tulip",
                "/setblock ~2 ~ ~-2 orange_tulip",
                "/setblock ~-2 ~ ~-2 oxeye_daisy",
            ],
            color="#E91E63",
            function_id="fun/flower_circle",
            bedrock_commands=[
                "/setblock ~3 ~ ~ red_flower",
                "/setblock ~-3 ~ ~ yellow_flower",
                "/setblock ~ ~ ~3 red_flower 1",
                "/setblock ~ ~ ~-3 red_flower 2",
                "/setblock ~2 ~ ~2 red_flower 3",
                "/setblock ~-2 ~ ~2 red_flower 4",
                "/setblock ~2 ~ ~-2 red_flower 5",
                "/setblock ~-2 ~ ~-2 red_flower 7",
            ]
        ),
    ]
)


# === CATEGORY 8: ADVANCED ===
ADVANCED = CommandCategory(
    name="Advanced",
    buttons=[
        CommandButton(
            name="Clone Area",
            description="Clone a 10x10x10 area 15 blocks away",
            commands=["/clone ~-5 ~-1 ~-5 ~5 ~9 ~5 ~10 ~-1 ~-5"],
            color="#546E7A",
            function_id="advanced/clone_area"
            # Same for Bedrock
        ),
        CommandButton(
            name="Mob Spawner",
            description="Get a monster spawner block",
            commands=["/give @s spawner 1"],
            color="#455A64",
            function_id="advanced/mob_spawner",
            bedrock_commands=["/give @s mob_spawner 1"]
        ),
        CommandButton(
            name="Command Block",
            description="Get a command block (creative mode)",
            commands=[
                "/give @s command_block 1",
                "/give @s chain_command_block 1",
                "/give @s repeating_command_block 1",
            ],
            color="#FF7043",
            function_id="advanced/command_block"
            # Same for Bedrock
        ),
        CommandButton(
            name="Structure Block",
            description="Get structure blocks for saving/loading builds",
            commands=["/give @s structure_block 4"],
            color="#8D6E63",
            function_id="advanced/structure_block"
            # Same for Bedrock
        ),
        CommandButton(
            name="Debug Stick",
            description="Tool to change block states (Java only)",
            commands=["/give @s debug_stick 1"],
            color="#7E57C2",
            function_id="advanced/debug_stick",
            bedrock_commands=[]  # Not available in Bedrock
        ),
        CommandButton(
            name="Barrier Blocks",
            description="Invisible solid blocks",
            commands=["/give @s barrier 64"],
            color="#B0BEC5",
            function_id="advanced/barrier_blocks"
            # Same for Bedrock
        ),
        CommandButton(
            name="Light Blocks",
            description="Invisible light sources (various levels)",
            commands=[
                "/give @s light 16",
            ],
            color="#FFF59D",
            function_id="advanced/light_blocks",
            bedrock_commands=["/give @s light_block 16"]
        ),
        CommandButton(
            name="XP Boost 1000",
            description="Add 1000 experience points",
            commands=["/xp add @s 1000 points"],
            color="#76FF03",
            function_id="advanced/xp_boost",
            bedrock_commands=["/xp 1000 @s"]
        ),
    ]
)


# All categories for easy iteration
ALL_CATEGORIES = [
    BUFFS_EFFECTS, GEAR_ITEMS, TELEPORT_LOCATE, WORLD_CONTROL,
    BUILDING_CREATION, FRIENDLY_MOBS, FUN_COSMETIC, ADVANCED
]
