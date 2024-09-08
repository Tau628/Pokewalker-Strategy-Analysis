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

## Model Used
A Markov decision process (MDP) was chosen to model these battles. The MDP consists of the following:

| Component | Description |
| -------- | ------- |
| States | The 16 possible combinations of health for the Player and the Wild Pokémon; plus a `Caught` state and a `Failed` state. |
| Actions | The actions `attack`, `evade`, and `catch`, corresponding the the three actions the player can take. |
| Reward function | Reward is 1 for the `Caught` state, -1 for the `Failed` state, and 0 for all others. |
| State transition matrix | As determined by game mechanics. To be detailed below. |
| Discount factor | 0.9 |

### Transition Probability Matrix
Assume $W_{a}(H_{player}, H_{wild})$ is the probability of the wild action $a\in \{ attack, evade, run \}$ for a given player health value and wild health value, $H_{player}$ and $H_{wild}$ respectively. Similarly $C(H_{wild})$ is the probability of a sucessful catch upon a player catch action for wild health value $H_{wild}$.

Then our state transition probability matrix can be described as follows.

- The `Caught` states and the `Failed` states return to themselves with probability 1, regardless of player action.
- When the player attacks at state $(H_{player}, H_{wild})$ the state transitions are
  - To $(H_{player}-1, H_{wild}-1)$ with probability $W_{attack}(H_{player}, H_{wild})$
  - To $(H_{player}-1, H_{wild})$ with probability $W_{evade}(H_{player}, H_{wild})$
  - To $(H_{player}-1, H_{wild}-2)$ with probability $W_{run}(H_{player}, H_{wild})$
- When the player evades at state $(H_{player}, H_{wild})$ the state transitions are
  - To $(H_{player}, H_{wild}-1)$ with probability $W_{attack}(H_{player}, H_{wild})$
  - To $(H_{player}, H_{wild})$ with probability $W_{evade}(H_{player}, H_{wild})$
  - To `Failed` with probability $W_{run}(H_{player}, H_{wild})$
- When the player catches at state $(H_{player}, H_{wild})$ the state transitions are
  - To `Caught` with probability $C(H_{wild})$
  - To `Failed` with probability $1 - C(H_{wild})$

This model assumes the following,
- $\sum_{a} W_{a}(H_{player}, H_{wild}) = 1, \forall H_{player}, H_{wild}$
- The probabilty of a wild action only depends on the current state of the game (that is, the health of both the player and wild Pokémon, not including the player's current action).
- The probabily of a sucessful catch only depends on the current health of the wild Pokémon.

### Probabilities Used
The currently ongoing work is finding the probabilities $W_{a}(H_{player}, H_{wild})$ and $C(H_{wild})$. Having found no documentation online about these probabilities, I have started collecting data. Currently, the best estimate for the probabilities are,

| $a$ | $W_{a}(H_{player}, H_{wild})$ |
| -------- | ------- |
| `attack` | 0.40 |
| `evade` | 0.35 |
| `run` | 0.25 |

$C(H_{wild})$
| $H_{wild}$ | $C(H_{wild})$ |
| -------- | ------- |
| 4 | 1/8 |
| 3 | 1/3 |
| 2| 2/3 |
| 1 | 9/10 |

This data is not accurate as I've been able to determine that $W_{a}(H_{player}, H_{wild})$ does depend on the health, but I have not collected enough data to determine each of the individual probabilities.
