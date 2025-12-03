# Example: Vanilla Netherite Gear (Voidwalker Regalia)

> **Note**: This is a user-contributed example showing how to create powerful vanilla Netherite gear with custom attributes using Maricraft. Replace `edwinald` with your player name.

**Theme**: Void/Cosmic - Otherworldly power from beyond the stars
**Minecraft Version**: 1.21.1 (NeoForge)
**Player**: edwinald

---

## The Voidwalker Regalia

*Forged in the space between dimensions, where light fears to tread and stars die screaming. This armor channels the raw entropy of the cosmos.*

---

## Armor Set

### Crown of the Void (Helmet)
```mcfunction
/give edwinald netherite_helmet[custom_name='{"text":"Crown of the Void","color":"dark_purple","bold":true}',enchantments={protection:4,respiration:3,aqua_affinity:1},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:5,operation:"add_value",slot:"head",id:"vw:a"},{type:"minecraft:generic.max_health",amount:10,operation:"add_value",slot:"head",id:"vw:h"}]] 1
```

### Nebula Heart Plate (Chestplate)
```mcfunction
/give edwinald netherite_chestplate[custom_name='{"text":"Nebula Heart Plate","color":"dark_purple","bold":true}',enchantments={protection:4,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:12,operation:"add_value",slot:"chest",id:"vw:a"},{type:"minecraft:generic.armor_toughness",amount:8,operation:"add_value",slot:"chest",id:"vw:t"},{type:"minecraft:generic.max_health",amount:20,operation:"add_value",slot:"chest",id:"vw:h"}]] 1
```

### Eclipse Stride (Leggings)
```mcfunction
/give edwinald netherite_leggings[custom_name='{"text":"Eclipse Stride","color":"blue","bold":true}',enchantments={protection:4,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:10,operation:"add_value",slot:"legs",id:"vw:a"},{type:"minecraft:generic.armor_toughness",amount:4,operation:"add_value",slot:"legs",id:"vw:t"}]] 1
```

### Starfall Treads (Boots)
```mcfunction
/give edwinald netherite_boots[custom_name='{"text":"Starfall Treads","color":"blue","bold":true}',enchantments={protection:4,feather_falling:4,depth_strider:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:5,operation:"add_value",slot:"feet",id:"vw:a"},{type:"minecraft:generic.movement_speed",amount:0.06,operation:"add_value",slot:"feet",id:"vw:s"}]] 1
```

---

## Weapons

### Entropy's Edge (Sword)
*The blade that cuts through reality itself*
```mcfunction
/give edwinald netherite_sword[custom_name='{"text":"Entropy\\u0027s Edge","color":"dark_purple","bold":true}',enchantments={sharpness:5,fire_aspect:2,knockback:2,sweeping_edge:3,looting:3,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.attack_damage",amount:2048,operation:"add_value",slot:"mainhand",id:"ee:d"},{type:"minecraft:generic.attack_speed",amount:2,operation:"add_value",slot:"mainhand",id:"ee:s"}]] 1
```

### Astral Piercer (Trident)
*Calls down lightning from dying stars*
```mcfunction
/give edwinald trident[custom_name='{"text":"Astral Piercer","color":"light_purple","bold":true}',enchantments={loyalty:3,channeling:1,impaling:5,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.attack_damage",amount:1024,operation:"add_value",slot:"mainhand",id:"ap:d"}]] 1
```

---

## Quick Deploy (All Commands)

Copy all commands below into Maricraft and run:

```mcfunction
/give edwinald netherite_helmet[custom_name='{"text":"Crown of the Void","color":"dark_purple","bold":true}',enchantments={protection:4,respiration:3,aqua_affinity:1},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:5,operation:"add_value",slot:"head",id:"vw:a"},{type:"minecraft:generic.max_health",amount:10,operation:"add_value",slot:"head",id:"vw:h"}]] 1
/give edwinald netherite_chestplate[custom_name='{"text":"Nebula Heart Plate","color":"dark_purple","bold":true}',enchantments={protection:4,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:12,operation:"add_value",slot:"chest",id:"vw:a"},{type:"minecraft:generic.armor_toughness",amount:8,operation:"add_value",slot:"chest",id:"vw:t"},{type:"minecraft:generic.max_health",amount:20,operation:"add_value",slot:"chest",id:"vw:h"}]] 1
/give edwinald netherite_leggings[custom_name='{"text":"Eclipse Stride","color":"blue","bold":true}',enchantments={protection:4,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:10,operation:"add_value",slot:"legs",id:"vw:a"},{type:"minecraft:generic.armor_toughness",amount:4,operation:"add_value",slot:"legs",id:"vw:t"}]] 1
/give edwinald netherite_boots[custom_name='{"text":"Starfall Treads","color":"blue","bold":true}',enchantments={protection:4,feather_falling:4,depth_strider:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.armor",amount:5,operation:"add_value",slot:"feet",id:"vw:a"},{type:"minecraft:generic.movement_speed",amount:0.06,operation:"add_value",slot:"feet",id:"vw:s"}]] 1
/give edwinald netherite_sword[custom_name='{"text":"Entropy\\u0027s Edge","color":"dark_purple","bold":true}',enchantments={sharpness:5,fire_aspect:2,knockback:2,sweeping_edge:3,looting:3,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.attack_damage",amount:2048,operation:"add_value",slot:"mainhand",id:"ee:d"},{type:"minecraft:generic.attack_speed",amount:2,operation:"add_value",slot:"mainhand",id:"ee:s"}]] 1
/give edwinald trident[custom_name='{"text":"Astral Piercer","color":"light_purple","bold":true}',enchantments={loyalty:3,channeling:1,impaling:5,unbreaking:3},unbreakable={},attribute_modifiers=[{type:"minecraft:generic.attack_damage",amount:1024,operation:"add_value",slot:"mainhand",id:"ap:d"}]] 1
```

---

## Stats Summary

| Item | Armor | Toughness | Health | Speed | Damage |
|------|-------|-----------|--------|-------|--------|
| Crown of the Void | +5 | - | +10 | - | - |
| Nebula Heart Plate | +12 | +8 | +20 | - | - |
| Eclipse Stride | +10 | +4 | - | - | - |
| Starfall Treads | +5 | - | - | +30% | - |
| **Armor Total** | **+32** | **+12** | **+30** | **+30%** | - |
| Entropy's Edge | - | - | - | - | +2048 |
| Astral Piercer | - | - | - | - | +1024 |

---

## Compact Versions (Chat-Safe, <256 chars)

If the full commands fail, use these simplified versions:

```mcfunction
/give edwinald netherite_helmet[custom_name='{"text":"Crown of the Void","color":"dark_purple","bold":true}',enchantments={protection:4,respiration:3},unbreakable={}] 1
/give edwinald netherite_chestplate[custom_name='{"text":"Nebula Heart","color":"dark_purple","bold":true}',enchantments={protection:4},unbreakable={}] 1
/give edwinald netherite_leggings[custom_name='{"text":"Eclipse Stride","color":"blue","bold":true}',enchantments={protection:4},unbreakable={}] 1
/give edwinald netherite_boots[custom_name='{"text":"Starfall Treads","color":"blue","bold":true}',enchantments={protection:4,feather_falling:4},unbreakable={}] 1
/give edwinald netherite_sword[custom_name='{"text":"Entropy Edge","color":"dark_purple","bold":true}',enchantments={sharpness:5,fire_aspect:2},unbreakable={}] 1
/give edwinald trident[custom_name='{"text":"Astral Piercer","color":"light_purple","bold":true}',enchantments={loyalty:3,channeling:1},unbreakable={}] 1
```

Then add power with `/enchant` and effects:
```mcfunction
/effect give edwinald minecraft:resistance 99999 3 true
/effect give edwinald minecraft:strength 99999 4 true
/effect give edwinald minecraft:speed 99999 2 true
/effect give edwinald minecraft:regeneration 99999 2 true
/effect give edwinald minecraft:health_boost 99999 4 true
```

---

## Notes

- All items are **unbreakable** - they will never lose durability
- Commands use 1.21.1 syntax with `minecraft:generic.*` attribute IDs
- Full commands exceed 256 characters - use compact versions for chat or command blocks for full versions
- The Trident has **Channeling** (summons lightning on hit during storms) + **Loyalty** (returns when thrown)
- Sword with Sharpness V + Fire Aspect II deals massive damage
- Effect commands give permanent buffs: resistance, strength, speed, regen, +10 hearts

