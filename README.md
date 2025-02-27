# Rime DPS Simulator

This project is a simple DPS simulator for the game Fellowship. It is a work in progress and does not yet include all features.

## 🚧 Work in Progress

Currently working on:

| Feature         | Status            |
| --------------- | ----------------- |
| AoE DPS         | ⚙️ In Progress     |
| Rotation Opener | 💡 To be Discussed |

## 📝 Notes

I wont offer any help running or using this software. If you are unfamiliar with Python, I'm sorry but I can't help.

## 🚀 How to Run

The program supports multiple arguments:

```bash
python main.py -s average_dps -e 5 -t <talent_tree> -p <preset> -c <custom_character>
```

- `-s <sim_type>`: The type of simulation to run.
- `-e <enemy_count>`: The number of enemies to simulate.
- `-t <talent_tree>`: The talent tree to use. Format must be `{row1}-{row2}-{row3}`.
- `-p <preset>`: Use a preset character.
- `-c <custom_character>`: Use a custom character. Format must be `{intellect}-{crit}-{expertise}-{haste}-{spirit}`.

### ✨ Example

```bash
python main.py -s average_dps -e 5 -t 2-12-3 -p default -c 100-20-30-40-50
```

This will run the average DPS simulation with 5 enemies, using the default preset and a custom character with 100 intellect, 20 crit, 30 expertise, 40 haste, and 50 spirit.
