"""Pre-defined Minecraft command buttons organized by category."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class CommandButton:
    """A single button that executes one or more commands."""
    name: str
    description: str
    commands: List[str]  # Java Edition commands
    color: str = "#3498DB"
    function_id: str = ""  # e.g., "maricraft:buffs/god_mode"
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
            function_id="maricraft:buffs/full_heal",
            bedrock_commands=["/effect @s instant_health 1 255"]
        ),
        CommandButton(
            name="Super Regen",
            description="Fast regeneration for 5 minutes",
            commands=["/effect give @s regeneration 300 2 true"],
            color="#4ECDC4",
            function_id="maricraft:buffs/super_regen",
            bedrock_commands=["/effect @s regeneration 300 2 true"]
        ),
        CommandButton(
            name="Health Boost",
            description="Extra hearts for 10 minutes",
            commands=["/effect give @s health_boost 600 4 true"],
            color="#E74C3C",
            function_id="maricraft:buffs/health_boost",
            bedrock_commands=["/effect @s health_boost 600 4 true"]
        ),
        CommandButton(
            name="Night Vision",
            description="See in the dark for 10 minutes",
            commands=["/effect give @s night_vision 600 0 true"],
            color="#9B59B6",
            function_id="maricraft:buffs/night_vision",
            bedrock_commands=["/effect @s night_vision 600 0 true"]
        ),
        CommandButton(
            name="Speed Boost",
            description="Run super fast for 5 minutes",
            commands=["/effect give @s speed 300 2 true"],
            color="#3498DB",
            function_id="maricraft:buffs/speed_boost",
            bedrock_commands=["/effect @s speed 300 2 true"]
        ),
        CommandButton(
            name="Jump Boost",
            description="Jump really high for 5 minutes",
            commands=["/effect give @s jump_boost 300 2 true"],
            color="#2ECC71",
            function_id="maricraft:buffs/jump_boost",
            bedrock_commands=["/effect @s jump_boost 300 2 true"]
        ),
        CommandButton(
            name="Water Breathing",
            description="Breathe underwater for 10 minutes",
            commands=["/effect give @s water_breathing 600 0 true"],
            color="#00CED1",
            function_id="maricraft:buffs/water_breathing",
            bedrock_commands=["/effect @s water_breathing 600 0 true"]
        ),
        CommandButton(
            name="Fire Resistance",
            description="Immune to fire for 10 minutes",
            commands=["/effect give @s fire_resistance 600 0 true"],
            color="#E67E22",
            function_id="maricraft:buffs/fire_resistance",
            bedrock_commands=["/effect @s fire_resistance 600 0 true"]
        ),
        CommandButton(
            name="Slow Falling",
            description="Fall slowly for 5 minutes",
            commands=["/effect give @s slow_falling 300 0 true"],
            color="#F1C40F",
            function_id="maricraft:buffs/slow_falling",
            bedrock_commands=["/effect @s slow_falling 300 0 true"]
        ),
        CommandButton(
            name="Invisibility",
            description="Become invisible for 5 minutes",
            commands=["/effect give @s invisibility 300 0 true"],
            color="#95A5A6",
            function_id="maricraft:buffs/invisibility",
            bedrock_commands=["/effect @s invisibility 300 0 true"]
        ),
        CommandButton(
            name="Resistance",
            description="Take less damage for 5 minutes",
            commands=["/effect give @s resistance 300 2 true"],
            color="#7F8C8D",
            function_id="maricraft:buffs/resistance",
            bedrock_commands=["/effect @s resistance 300 2 true"]
        ),
        CommandButton(
            name="Strength",
            description="Deal more damage for 5 minutes",
            commands=["/effect give @s strength 300 2 true"],
            color="#C0392B",
            function_id="maricraft:buffs/strength",
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
            function_id="maricraft:buffs/god_mode",
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
            function_id="maricraft:buffs/clear_effects",
            bedrock_commands=["/effect @s clear"]
        ),
        CommandButton(
            name="Saturation",
            description="Never get hungry for 10 minutes",
            commands=["/effect give @s saturation 600 0 true"],
            color="#F39C12",
            function_id="maricraft:buffs/saturation",
            bedrock_commands=["/effect @s saturation 600 0 true"]
        ),
        CommandButton(
            name="Haste",
            description="Mine faster for 5 minutes",
            commands=["/effect give @s haste 300 2 true"],
            color="#1ABC9C",
            function_id="maricraft:buffs/haste",
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
            function_id="maricraft:gear/diamond_armor"
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
            function_id="maricraft:gear/netherite_armor"
            # Same for Bedrock - no enchantments needed
        ),
        CommandButton(
            name="Super Sword",
            description="Netherite sword with best enchants",
            commands=[
                '/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2,looting:3,unbreaking:3,mending:1}}] 1'
            ],
            color="#8E44AD",
            function_id="maricraft:gear/super_sword",
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
            function_id="maricraft:gear/super_bow",
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
            function_id="maricraft:gear/super_pickaxe",
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
            function_id="maricraft:gear/super_axe",
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
            function_id="maricraft:gear/elytra_rockets",
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
            function_id="maricraft:gear/trident",
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
            function_id="maricraft:gear/shield",
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
            function_id="maricraft:gear/golden_apples"
            # Same for Bedrock
        ),
        CommandButton(
            name="Enchanted Apples",
            description="Stack of enchanted golden apples (Notch apples)",
            commands=["/give @s enchanted_golden_apple 64"],
            color="#FFD700",
            function_id="maricraft:gear/enchanted_apples"
            # Same for Bedrock
        ),
        CommandButton(
            name="Ender Pearls",
            description="Stack of 16 ender pearls",
            commands=["/give @s ender_pearl 16"],
            color="#2C3E50",
            function_id="maricraft:gear/ender_pearls"
            # Same for Bedrock
        ),
        CommandButton(
            name="Totem of Undying",
            description="Saves you from death",
            commands=["/give @s totem_of_undying 1"],
            color="#27AE60",
            function_id="maricraft:gear/totem"
            # Same for Bedrock
        ),
        CommandButton(
            name="Crossbow",
            description="Quick charge crossbow with multishot",
            commands=[
                '/give @s crossbow[enchantments={levels:{quick_charge:3,multishot:1,unbreaking:3}}] 1'
            ],
            color="#6C5B7B",
            function_id="maricraft:gear/crossbow",
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
            function_id="maricraft:gear/full_tool_set",
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
            function_id="maricraft:gear/steak"
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
            function_id="maricraft:teleport/find_village",
            bedrock_commands=["/locate structure village"]
        ),
        CommandButton(
            name="Find Stronghold",
            description="Locate the End portal",
            commands=["/locate structure stronghold"],
            color="#607D8B",
            function_id="maricraft:teleport/find_stronghold",
            bedrock_commands=["/locate structure stronghold"]
        ),
        CommandButton(
            name="Find Mansion",
            description="Locate woodland mansion",
            commands=["/locate structure mansion"],
            color="#795548",
            function_id="maricraft:teleport/find_mansion",
            bedrock_commands=["/locate structure mansion"]
        ),
        CommandButton(
            name="Find Monument",
            description="Locate ocean monument",
            commands=["/locate structure monument"],
            color="#00ACC1",
            function_id="maricraft:teleport/find_monument",
            bedrock_commands=["/locate structure monument"]
        ),
        CommandButton(
            name="Find Fortress",
            description="Locate nether fortress (use in Nether)",
            commands=["/locate structure fortress"],
            color="#B71C1C",
            function_id="maricraft:teleport/find_fortress",
            bedrock_commands=["/locate structure fortress"]
        ),
        CommandButton(
            name="Find Bastion",
            description="Locate bastion remnant (use in Nether)",
            commands=["/locate structure bastion_remnant"],
            color="#424242",
            function_id="maricraft:teleport/find_bastion",
            bedrock_commands=["/locate structure bastion_remnant"]
        ),
        CommandButton(
            name="Find Temple",
            description="Locate desert or jungle temple",
            commands=["/locate structure desert_pyramid"],
            color="#FFB74D",
            function_id="maricraft:teleport/find_temple",
            bedrock_commands=["/locate structure desert_pyramid"]
        ),
        CommandButton(
            name="Find Mineshaft",
            description="Locate abandoned mineshaft",
            commands=["/locate structure mineshaft"],
            color="#8D6E63",
            function_id="maricraft:teleport/find_mineshaft",
            bedrock_commands=["/locate structure mineshaft"]
        ),
        CommandButton(
            name="TP to Spawn",
            description="Teleport to world spawn (0, ?, 0)",
            commands=["/tp @s 0 100 0"],
            color="#4CAF50",
            function_id="maricraft:teleport/tp_spawn"
            # Same for Bedrock
        ),
        CommandButton(
            name="TP Up 50",
            description="Teleport 50 blocks up",
            commands=["/tp @s ~ ~50 ~"],
            color="#03A9F4",
            function_id="maricraft:teleport/tp_up_50"
            # Same for Bedrock
        ),
        CommandButton(
            name="TP Forward 100",
            description="Teleport 100 blocks forward (where you're looking)",
            commands=["/execute at @s run tp @s ^0 ^0 ^100"],
            color="#9C27B0",
            function_id="maricraft:teleport/tp_forward_100",
            bedrock_commands=["/execute @s ~~~ tp @s ^0 ^0 ^100"]
        ),
        CommandButton(
            name="TP Back 75",
            description="Teleport 75 blocks backward",
            commands=["/execute at @s run tp @s ^0 ^0 ^-75"],
            color="#FF5722",
            function_id="maricraft:teleport/tp_back_75",
            bedrock_commands=["/execute @s ~~~ tp @s ^0 ^0 ^-75"]
        ),
        CommandButton(
            name="TP to Surface",
            description="Teleport to highest block at your position",
            commands=["/tp @s ~ 320 ~", "/effect give @s slow_falling 10 0 true"],
            color="#81C784",
            function_id="maricraft:teleport/tp_surface",
            bedrock_commands=["/tp @s ~ 320 ~", "/effect @s slow_falling 10 0 true"]
        ),
        CommandButton(
            name="Find End City",
            description="Locate end city (use in The End)",
            commands=["/locate structure end_city"],
            color="#CE93D8",
            function_id="maricraft:teleport/find_end_city",
            bedrock_commands=["/locate structure end_city"]
        ),
        CommandButton(
            name="Find Trail Ruins",
            description="Locate trail ruins",
            commands=["/locate structure trail_ruins"],
            color="#BCAAA4",
            function_id="maricraft:teleport/find_trail_ruins",
            bedrock_commands=["/locate structure trail_ruins"]
        ),
        CommandButton(
            name="Find Ancient City",
            description="Locate ancient city (deep underground)",
            commands=["/locate structure ancient_city"],
            color="#455A64",
            function_id="maricraft:teleport/find_ancient_city",
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
            function_id="maricraft:world/set_day"
        ),
        CommandButton(
            name="Set Noon",
            description="Change time to noon",
            commands=["/time set noon"],
            color="#FFEB3B",
            function_id="maricraft:world/set_noon"
        ),
        CommandButton(
            name="Set Night",
            description="Change time to night",
            commands=["/time set night"],
            color="#37474F",
            function_id="maricraft:world/set_night"
        ),
        CommandButton(
            name="Clear Weather",
            description="Stop rain and thunder",
            commands=["/weather clear"],
            color="#81D4FA",
            function_id="maricraft:world/clear_weather"
        ),
        CommandButton(
            name="Make Rain",
            description="Start raining",
            commands=["/weather rain"],
            color="#78909C",
            function_id="maricraft:world/make_rain"
        ),
        CommandButton(
            name="Thunderstorm",
            description="Start a thunderstorm",
            commands=["/weather thunder"],
            color="#455A64",
            function_id="maricraft:world/thunderstorm"
        ),
        CommandButton(
            name="Peaceful",
            description="No monsters spawn",
            commands=["/difficulty peaceful"],
            color="#A5D6A7",
            function_id="maricraft:world/peaceful"
        ),
        CommandButton(
            name="Easy Mode",
            description="Monsters do less damage",
            commands=["/difficulty easy"],
            color="#C5E1A5",
            function_id="maricraft:world/easy_mode"
        ),
        CommandButton(
            name="Normal Mode",
            description="Normal monster difficulty",
            commands=["/difficulty normal"],
            color="#FFCC80",
            function_id="maricraft:world/normal_mode"
        ),
        CommandButton(
            name="Hard Mode",
            description="Monsters do more damage",
            commands=["/difficulty hard"],
            color="#EF9A9A",
            function_id="maricraft:world/hard_mode"
        ),
        CommandButton(
            name="Creative Mode",
            description="Fly and infinite items",
            commands=["/gamemode creative"],
            color="#CE93D8",
            function_id="maricraft:world/creative_mode"
        ),
        CommandButton(
            name="Survival Mode",
            description="Normal survival gameplay",
            commands=["/gamemode survival"],
            color="#90CAF9",
            function_id="maricraft:world/survival_mode"
        ),
        CommandButton(
            name="Spectator Mode",
            description="Fly through blocks invisibly",
            commands=["/gamemode spectator"],
            color="#B0BEC5",
            function_id="maricraft:world/spectator_mode"
        ),
        CommandButton(
            name="Keep Inventory",
            description="Keep items when you die",
            commands=["/gamerule keepInventory true"],
            color="#80CBC4",
            function_id="maricraft:world/keep_inventory"
        ),
        CommandButton(
            name="Kill Hostiles",
            description="Remove hostile mobs nearby",
            commands=["/kill @e[type=#minecraft:raiders,distance=..100]"],
            color="#E57373",
            function_id="maricraft:world/kill_hostiles",
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
            function_id="maricraft:world/freeze_time"
        ),
    ]
)


# All categories for easy iteration
ALL_CATEGORIES = [BUFFS_EFFECTS, GEAR_ITEMS, TELEPORT_LOCATE, WORLD_CONTROL]
