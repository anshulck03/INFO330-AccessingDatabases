import sqlite3
import sys

# All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]

# Take six parameters on the command-line
if len(sys.argv) != 7:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
conn = sqlite3.connect('Pokemon.sqlite')
cur = conn.cursor()

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    if arg.isdigit():
        cur.execute("SELECT * FROM pokemon WHERE pokedex_number=?", (arg,))
    else:
        cur.execute("SELECT * FROM pokemon WHERE name=?", (arg.capitalize(),))

    pokemon = cur.fetchone()

    if not pokemon:
        print(f"Pokedex number or Pokemon name {arg} not found.")
        sys.exit()

    strong_against = []
    weak_against = []

    for t in types:
        against_value = pokemon[types.index(t) + 1]
        if against_value > 1:
            strong_against.append(t)
        elif against_value < 1:
            weak_against.append(t)

    print(f"Analyzing {arg}")
    print(f"{pokemon[1]} ({pokemon[2]} {pokemon[3]}) is strong against {strong_against} but weak against {weak_against}")
    team.append(pokemon)

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    for pokemon in team:
        cur.execute("INSERT INTO teams (team_name, pokedex_number) VALUES (?, ?)", (teamName, pokemon[0]))

    conn.commit()
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

conn.close()
