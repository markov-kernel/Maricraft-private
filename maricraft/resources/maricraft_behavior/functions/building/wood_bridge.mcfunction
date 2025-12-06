# Maricraft: Wood Bridge 20 (Bedrock Edition)
# Builds a wooden bridge 20 blocks in front of the player
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

fill ^-1 ^-1 ^1 ^1 ^-1 ^20 oak_planks

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]