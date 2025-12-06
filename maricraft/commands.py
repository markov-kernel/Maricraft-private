"""Pre-defined Minecraft command buttons organized by category."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class CommandButton:
    """A single button that executes one or more commands."""
    name: str
    description: str
    commands: List[str]
    color: str = "#3498DB"


@dataclass
class CommandCategory:
    """A category of related command buttons."""
    name: str
    buttons: List[CommandButton] = field(default_factory=list)


# === CATEGORY 1: BUFFS & EFFECTS ===
BUFFS_EFFECTS = CommandCategory(
    name="Buffs & Effects",
    buttons=[
        CommandButton(
            name="Full Heal",
            description="Restore all health instantly",
            commands=["/effect give @s instant_health 1 255"],
            color="#FF6B6B"
        ),
        CommandButton(
            name="Super Regen",
            description="Fast regeneration for 5 minutes",
            commands=["/effect give @s regeneration 300 2 true"],
            color="#4ECDC4"
        ),
        CommandButton(
            name="Health Boost",
            description="Extra hearts for 10 minutes",
            commands=["/effect give @s health_boost 600 4 true"],
            color="#E74C3C"
        ),
        CommandButton(
            name="Night Vision",
            description="See in the dark for 10 minutes",
            commands=["/effect give @s night_vision 600 0 true"],
            color="#9B59B6"
        ),
        CommandButton(
            name="Speed Boost",
            description="Run super fast for 5 minutes",
            commands=["/effect give @s speed 300 2 true"],
            color="#3498DB"
        ),
        CommandButton(
            name="Jump Boost",
            description="Jump really high for 5 minutes",
            commands=["/effect give @s jump_boost 300 2 true"],
            color="#2ECC71"
        ),
        CommandButton(
            name="Water Breathing",
            description="Breathe underwater for 10 minutes",
            commands=["/effect give @s water_breathing 600 0 true"],
            color="#00CED1"
        ),
        CommandButton(
            name="Fire Resistance",
            description="Immune to fire for 10 minutes",
            commands=["/effect give @s fire_resistance 600 0 true"],
            color="#E67E22"
        ),
        CommandButton(
            name="Slow Falling",
            description="Fall slowly for 5 minutes",
            commands=["/effect give @s slow_falling 300 0 true"],
            color="#F1C40F"
        ),
        CommandButton(
            name="Invisibility",
            description="Become invisible for 5 minutes",
            commands=["/effect give @s invisibility 300 0 true"],
            color="#95A5A6"
        ),
        CommandButton(
            name="Resistance",
            description="Take less damage for 5 minutes",
            commands=["/effect give @s resistance 300 2 true"],
            color="#7F8C8D"
        ),
        CommandButton(
            name="Strength",
            description="Deal more damage for 5 minutes",
            commands=["/effect give @s strength 300 2 true"],
            color="#C0392B"
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
            color="#FFD700"
        ),
        CommandButton(
            name="Clear Effects",
            description="Remove all active effects",
            commands=["/effect clear @s"],
            color="#BDC3C7"
        ),
        CommandButton(
            name="Saturation",
            description="Never get hungry for 10 minutes",
            commands=["/effect give @s saturation 600 0 true"],
            color="#F39C12"
        ),
        CommandButton(
            name="Haste",
            description="Mine faster for 5 minutes",
            commands=["/effect give @s haste 300 2 true"],
            color="#1ABC9C"
        ),
    ]
)


# === CATEGORY 2: GEAR & ITEMS ===
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
            color="#00BFFF"
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
            color="#4A4A4A"
        ),
        CommandButton(
            name="Super Sword",
            description="Netherite sword with best enchants",
            commands=[
                '/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2,looting:3,unbreaking:3,mending:1}}] 1'
            ],
            color="#8E44AD"
        ),
        CommandButton(
            name="Super Bow",
            description="Bow with power 5 and infinity",
            commands=[
                '/give @s bow[enchantments={levels:{power:5,flame:1,infinity:1,unbreaking:3}}] 1',
                "/give @s arrow 64",
            ],
            color="#D35400"
        ),
        CommandButton(
            name="Super Pickaxe",
            description="Netherite pickaxe for fast mining",
            commands=[
                '/give @s netherite_pickaxe[enchantments={levels:{efficiency:5,fortune:3,unbreaking:3,mending:1}}] 1'
            ],
            color="#1ABC9C"
        ),
        CommandButton(
            name="Super Axe",
            description="Netherite axe with sharpness",
            commands=[
                '/give @s netherite_axe[enchantments={levels:{sharpness:5,efficiency:5,unbreaking:3,mending:1}}] 1'
            ],
            color="#795548"
        ),
        CommandButton(
            name="Elytra + Rockets",
            description="Wings to fly plus firework rockets",
            commands=[
                '/give @s elytra[unbreakable={}] 1',
                "/give @s firework_rocket 64",
            ],
            color="#9B59B6"
        ),
        CommandButton(
            name="Trident",
            description="Trident with loyalty and channeling",
            commands=[
                '/give @s trident[enchantments={levels:{loyalty:3,channeling:1,impaling:5,unbreaking:3}}] 1'
            ],
            color="#3498DB"
        ),
        CommandButton(
            name="Shield",
            description="Unbreakable shield",
            commands=['/give @s shield[unbreakable={}] 1'],
            color="#7F8C8D"
        ),
        CommandButton(
            name="Golden Apples",
            description="Stack of 64 golden apples",
            commands=["/give @s golden_apple 64"],
            color="#F1C40F"
        ),
        CommandButton(
            name="Enchanted Apples",
            description="Stack of enchanted golden apples (Notch apples)",
            commands=["/give @s enchanted_golden_apple 64"],
            color="#FFD700"
        ),
        CommandButton(
            name="Ender Pearls",
            description="Stack of 16 ender pearls",
            commands=["/give @s ender_pearl 16"],
            color="#2C3E50"
        ),
        CommandButton(
            name="Totem of Undying",
            description="Saves you from death",
            commands=["/give @s totem_of_undying 1"],
            color="#27AE60"
        ),
        CommandButton(
            name="Crossbow",
            description="Quick charge crossbow with multishot",
            commands=[
                '/give @s crossbow[enchantments={levels:{quick_charge:3,multishot:1,unbreaking:3}}] 1'
            ],
            color="#6C5B7B"
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
            color="#34495E"
        ),
        CommandButton(
            name="Steak x64",
            description="Stack of cooked steak",
            commands=["/give @s cooked_beef 64"],
            color="#A93226"
        ),
    ]
)


# === CATEGORY 3: TELEPORT & LOCATE ===
TELEPORT_LOCATE = CommandCategory(
    name="Teleport & Locate",
    buttons=[
        CommandButton(
            name="Find Village",
            description="Locate nearest village",
            commands=["/locate structure village"],
            color="#8D6E63"
        ),
        CommandButton(
            name="Find Stronghold",
            description="Locate the End portal",
            commands=["/locate structure stronghold"],
            color="#607D8B"
        ),
        CommandButton(
            name="Find Mansion",
            description="Locate woodland mansion",
            commands=["/locate structure mansion"],
            color="#795548"
        ),
        CommandButton(
            name="Find Monument",
            description="Locate ocean monument",
            commands=["/locate structure monument"],
            color="#00ACC1"
        ),
        CommandButton(
            name="Find Fortress",
            description="Locate nether fortress (use in Nether)",
            commands=["/locate structure fortress"],
            color="#B71C1C"
        ),
        CommandButton(
            name="Find Bastion",
            description="Locate bastion remnant (use in Nether)",
            commands=["/locate structure bastion_remnant"],
            color="#424242"
        ),
        CommandButton(
            name="Find Temple",
            description="Locate desert or jungle temple",
            commands=["/locate structure desert_pyramid"],
            color="#FFB74D"
        ),
        CommandButton(
            name="Find Mineshaft",
            description="Locate abandoned mineshaft",
            commands=["/locate structure mineshaft"],
            color="#8D6E63"
        ),
        CommandButton(
            name="TP to Spawn",
            description="Teleport to world spawn (0, ?, 0)",
            commands=["/tp @s 0 100 0"],
            color="#4CAF50"
        ),
        CommandButton(
            name="TP Up 50",
            description="Teleport 50 blocks up",
            commands=["/tp @s ~ ~50 ~"],
            color="#03A9F4"
        ),
        CommandButton(
            name="TP Forward 100",
            description="Teleport 100 blocks forward (where you're looking)",
            commands=["/execute at @s run tp @s ^0 ^0 ^100"],
            color="#9C27B0"
        ),
        CommandButton(
            name="TP Back 75",
            description="Teleport 75 blocks backward",
            commands=["/execute at @s run tp @s ^0 ^0 ^-75"],
            color="#FF5722"
        ),
        CommandButton(
            name="TP to Surface",
            description="Teleport to highest block at your position",
            commands=["/tp @s ~ 320 ~", "/effect give @s slow_falling 10 0 true"],
            color="#81C784"
        ),
        CommandButton(
            name="Find End City",
            description="Locate end city (use in The End)",
            commands=["/locate structure end_city"],
            color="#CE93D8"
        ),
        CommandButton(
            name="Find Trail Ruins",
            description="Locate trail ruins",
            commands=["/locate structure trail_ruins"],
            color="#BCAAA4"
        ),
        CommandButton(
            name="Find Ancient City",
            description="Locate ancient city (deep underground)",
            commands=["/locate structure ancient_city"],
            color="#455A64"
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
            color="#FFD54F"
        ),
        CommandButton(
            name="Set Noon",
            description="Change time to noon",
            commands=["/time set noon"],
            color="#FFEB3B"
        ),
        CommandButton(
            name="Set Night",
            description="Change time to night",
            commands=["/time set night"],
            color="#37474F"
        ),
        CommandButton(
            name="Clear Weather",
            description="Stop rain and thunder",
            commands=["/weather clear"],
            color="#81D4FA"
        ),
        CommandButton(
            name="Make Rain",
            description="Start raining",
            commands=["/weather rain"],
            color="#78909C"
        ),
        CommandButton(
            name="Thunderstorm",
            description="Start a thunderstorm",
            commands=["/weather thunder"],
            color="#455A64"
        ),
        CommandButton(
            name="Peaceful",
            description="No monsters spawn",
            commands=["/difficulty peaceful"],
            color="#A5D6A7"
        ),
        CommandButton(
            name="Easy Mode",
            description="Monsters do less damage",
            commands=["/difficulty easy"],
            color="#C5E1A5"
        ),
        CommandButton(
            name="Normal Mode",
            description="Normal monster difficulty",
            commands=["/difficulty normal"],
            color="#FFCC80"
        ),
        CommandButton(
            name="Hard Mode",
            description="Monsters do more damage",
            commands=["/difficulty hard"],
            color="#EF9A9A"
        ),
        CommandButton(
            name="Creative Mode",
            description="Fly and infinite items",
            commands=["/gamemode creative"],
            color="#CE93D8"
        ),
        CommandButton(
            name="Survival Mode",
            description="Normal survival gameplay",
            commands=["/gamemode survival"],
            color="#90CAF9"
        ),
        CommandButton(
            name="Spectator Mode",
            description="Fly through blocks invisibly",
            commands=["/gamemode spectator"],
            color="#B0BEC5"
        ),
        CommandButton(
            name="Keep Inventory",
            description="Keep items when you die",
            commands=["/gamerule keepInventory true"],
            color="#80CBC4"
        ),
        CommandButton(
            name="Kill Hostiles",
            description="Remove hostile mobs nearby",
            commands=["/kill @e[type=#minecraft:raiders,distance=..100]"],
            color="#E57373"
        ),
        CommandButton(
            name="Freeze Time",
            description="Stop the day/night cycle",
            commands=["/gamerule doDaylightCycle false"],
            color="#B39DDB"
        ),
    ]
)


# All categories for easy iteration
ALL_CATEGORIES = [BUFFS_EFFECTS, GEAR_ITEMS, TELEPORT_LOCATE, WORLD_CONTROL]
