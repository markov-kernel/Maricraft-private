# Maricraft: GOD MODE
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s regeneration 99999 4 true
effect @s resistance 99999 4 true
effect @s strength 99999 2 true
effect @s speed 99999 1 true
effect @s fire_resistance 99999 0 true
effect @s night_vision 99999 0 true
effect @s health_boost 99999 4 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]