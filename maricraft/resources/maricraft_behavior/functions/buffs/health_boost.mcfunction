# Maricraft: Health Boost
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s health_boost 600 4 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]