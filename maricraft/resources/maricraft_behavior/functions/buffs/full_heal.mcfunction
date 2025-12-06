# Maricraft: Full Heal
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s instant_health 1 255

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]