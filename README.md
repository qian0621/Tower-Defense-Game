# Tower-Defense-Game
Undead creatures are attacking the city! Position your units to protect the city until you have killed enough of the creatures to drive them off.

In this “tower defence” strategy game, monsters are advancing on the city from right to left. To kill the monsters, you have to purchase units and place them on the field of battle. However, you start with 10 gold and only get 1 gold per turn, so spend your precious resources wisely!

## Monsters
### Zombie
Speed: 1\
Max HP: 15\
Reward: 2\
Damage: 3-6

### Werewolf
Speed: 2\
Max HP: 10\
Reward: 3\
Damage: 1-4

## Units:
### Wall:
Max HP: 20\
Value: 3\
Upgrade cost: 6\
HP and max HP will increase by 5

### Archer:
Max HP: 5\
Value: 5\
Damage: 1-4\
Upgrade cost: 8\
HP, max HP and damage range will increase by 1

### Cannon:
Max HP: 8\
Value: 7\
Firing Rate: /3 turns\
Damage: 7-10\
Push Probability: 40%\
Upgrade Cost: 10\
HP, max HP and damage range will increase by 1\
Push probability will increase by 10% till 100%\
Firing rate will decrease by 1 turn until Cannon fires every turn

### Mine:
Value: 8\
Triggered by being stepped on:\
Does 10 damage to nearby (3x3) squares\
Upgrade Cost: 2\
Increases damage by 2

**Upgrade cost increases by 3 gold per upgrade**

## Each turn:
1. Offensive units fire leftwards
2. Monsters advance towards the right and attack from left to right, up to down
3. Monsters spawn

Every 10 turns danger level increases:\
Monster max HP, damage range, and reward increases by 1
