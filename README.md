# Pokewalker-Strategy-Analysis
The Pokéwalker is a peripheral used with Pokémon HeartGold and SoulSilver. Players can transfer Pokémon from those games into the device to go on walks and play minigames. One minigame of interest is the Poké Radar, which allows for the capture of various Pokémon. This minigame uses highly simplified battle mechanics to facilitate these captures. This project attempts to use a Markov decision process (MDP) model find the optimal strategy for capturing Poké Radar Pokémon on the Pokéwalker.

## Poké Radar Battle Mechanics
Battles take place between a player Pokémon and a wild Pokémon. Each starts at 4 health points. The player Pokémon has three actions each turn: attack, evade, and catch. Similarly the wild Pokémon will pick between three actions: attack, evade, and catch. The outcome of each turn is dependent on the actions chosen. 

When the player chooses to attack:
| Wild Action | Result |
| -------- | ------- |
| Attack | Both Pokémon take one damage |
| Evade | Player's Pokémon takes one damage |
| Run | Player's Pokémon takes one damage and Wild Pokémon takes two damage |

When the player chooses to evade:
| Wild Action | Result |
| -------- | ------- |
| Attack | Wild Pokémon takes one damage |
| Evade | Nothing |
| Run | Wild Pokémon runs away |

And when the player chooses to catch, this results in a successful catch with some probability. Otherwise, the wild Pokémon runs away.

The encounter fails if either Pokemon is reduced to 0 health.
