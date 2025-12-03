# Example: Cataclysm Mod Gear (Cursium Arsenal)

> **Note**: This is a user-contributed example showing how to use Maricraft with modded items from the L_Ender's Cataclysm mod. Replace `edwinald` with your player name.

**Mod**: L_Ender's Cataclysm
**Minecraft Version**: 1.21.1 (NeoForge)
**Player**: edwinald

---

## About Cursium Armor

Cursium is an endgame armor tier from the **Cataclysm** mod. It's crafted from Cursium Ingots dropped by **Maledictus** in the Frosted Prison dungeon. The armor is inherently **unbreakable** and has unique abilities.

### Built-in Abilities

| Piece | Ability | Effect |
|-------|---------|--------|
| Helmet | **Ghost Vision** | Press C to mark nearby entities with glow (25 blocks, 7s) |
| Chestplate | **Undead Revive** | Prevents death once, restores 5 HP + invincibility (6min cooldown) |
| Leggings | **Ghost Dodge** | Chance to nullify damage, especially projectiles |
| Boots | **Ghostly Weightless** | Reduces fall damage, press V for backward leap |

---

## Full Armor Set Commands

### Cursium Helmet
```mcfunction
/give edwinald cataclysm:cursium_helmet[custom_name='{"text":"Maledictus Crown","color":"dark_aqua","bold":true}',enchantments={protection:4,respiration:3,aqua_affinity:1}] 1
```

### Cursium Chestplate
```mcfunction
/give edwinald cataclysm:cursium_chestplate[custom_name='{"text":"Soulbound Plate","color":"dark_aqua","bold":true}',enchantments={protection:4,thorns:3}] 1
```

### Cursium Leggings
```mcfunction
/give edwinald cataclysm:cursium_leggings[custom_name='{"text":"Phantom Stride","color":"dark_aqua","bold":true}',enchantments={protection:4,swift_sneak:3}] 1
```

### Cursium Boots
```mcfunction
/give edwinald cataclysm:cursium_boots[custom_name='{"text":"Wraithwalkers","color":"dark_aqua","bold":true}',enchantments={protection:4,feather_falling:4,depth_strider:3,soul_speed:3}] 1
```

---

## Cataclysm Weapons (Bonus)

### The Incinerator (Ignitium Sword)
```mcfunction
/give edwinald cataclysm:the_incinerator[custom_name='{"text":"Hellfire Render","color":"gold","bold":true}',enchantments={sharpness:5,fire_aspect:2,looting:3}] 1
```

### Void Forge (Cursium Sword - if available)
```mcfunction
/give edwinald cataclysm:cursium_sword[custom_name='{"text":"Soul Harvester","color":"dark_aqua","bold":true}',enchantments={sharpness:5,knockback:2,looting:3}] 1
```

### Gauntlet of Bulwark
```mcfunction
/give edwinald cataclysm:gauntlet_of_bulwark[custom_name='{"text":"Titan Fist","color":"gray","bold":true}'] 1
```

### Void Assault Shoulder Weapon
```mcfunction
/give edwinald cataclysm:void_assault_shoulder_weapon 1
```

---

## Quick Deploy (All Armor)

Copy into Maricraft:

```mcfunction
/give edwinald cataclysm:cursium_helmet[custom_name='{"text":"Maledictus Crown","color":"dark_aqua","bold":true}',enchantments={protection:4,respiration:3,aqua_affinity:1}] 1
/give edwinald cataclysm:cursium_chestplate[custom_name='{"text":"Soulbound Plate","color":"dark_aqua","bold":true}',enchantments={protection:4,thorns:3}] 1
/give edwinald cataclysm:cursium_leggings[custom_name='{"text":"Phantom Stride","color":"dark_aqua","bold":true}',enchantments={protection:4,swift_sneak:3}] 1
/give edwinald cataclysm:cursium_boots[custom_name='{"text":"Wraithwalkers","color":"dark_aqua","bold":true}',enchantments={protection:4,feather_falling:4,depth_strider:3,soul_speed:3}] 1
```

---

## Compact Versions (Vanilla-style, no custom names)

If custom names cause issues:

```mcfunction
/give edwinald cataclysm:cursium_helmet[enchantments={protection:4,respiration:3,aqua_affinity:1}] 1
/give edwinald cataclysm:cursium_chestplate[enchantments={protection:4,thorns:3}] 1
/give edwinald cataclysm:cursium_leggings[enchantments={protection:4,swift_sneak:3}] 1
/give edwinald cataclysm:cursium_boots[enchantments={protection:4,feather_falling:4,depth_strider:3}] 1
```

---

## Power Buffs

```mcfunction
/effect give edwinald minecraft:resistance 99999 3 true
/effect give edwinald minecraft:strength 99999 4 true
/effect give edwinald minecraft:speed 99999 2 true
/effect give edwinald minecraft:regeneration 99999 2 true
/effect give edwinald minecraft:health_boost 99999 4 true
/effect give edwinald minecraft:night_vision 99999 0 true
```

---

## Notes

- Cursium armor is **inherently unbreakable** (no need for unbreakable={})
- The mod namespace is `cataclysm:` - use Tab autocomplete in-game if items don't work
- Built-in abilities work automatically (Ghost Vision = C key, Backward Leap = V key)
- Colors: dark_aqua fits the ghostly/cursed theme of Cursium
- If playing on a server, ensure the Cataclysm mod is installed

---

## Sources

- [Cataclysm Wiki: Cursium Armor](https://www.minecraft-guides.com/wiki/cataclysm/frosted-prison/cursium-armor/)
- [L_Ender's Cataclysm on CurseForge](https://www.curseforge.com/minecraft/mc-mods/lendercataclysm)
- [L_Ender's Cataclysm on Modrinth](https://modrinth.com/mod/l_enders-cataclysm)

