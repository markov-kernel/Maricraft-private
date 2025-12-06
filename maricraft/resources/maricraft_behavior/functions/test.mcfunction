# Maricraft: Test Function
# Simple test to verify functions work
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

say Maricraft functions are working!
give @s diamond 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]