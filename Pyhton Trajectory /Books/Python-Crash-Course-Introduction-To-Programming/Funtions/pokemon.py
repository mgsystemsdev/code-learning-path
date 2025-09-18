class Charmander:
    def __init__(self):
        self.name = "Charmander"
        self.level = 5
        self.hp = 20
        self.attack = 8
        self.move = "Ember"

    def show_status(self):
        print(
            f"Hello I'm {self.name}. My current strength level is {self.level} and my hp is {self.hp}"
        )

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} took {damage} damage! HP is now {self.hp}")

    def use_attack(self, target):
        print(f"{self.name} used {self.move}!")
        damage = self.attack
        target.take_damage(damage)


# Create your Pokémon
pokemon = Charmander()
pokemon.show_status()

# Trainer interaction
name = input("Hello, what's your name? ")
trainer = input(f"Are you my new trainer, {name}? (yes/no) ")

if trainer.lower() == "yes":
    show_attack = input(f"That's fantastic {name}! Would you like to see my attacks?")

else:
    print("Oh... maybe another time then!")

# Example: Attack a wild Pokémon
enemy_pokemon = Charmander()
enemy_pokemon.name = "Wild Rattata"
pokemon.use_attack(enemy_pokemon)


def battle(pokemon1, pokemon2):
    while pokemon1.hp > 0 and pokemon2.hp > 0:
        pokemon1.use_attack(pokemon2)
        if pokemon2.hp <= 0:
            print(f"{pokemon2.name} fainted!")
