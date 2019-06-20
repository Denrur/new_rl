class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = list()

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = list()
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': f'{self.owner.name} attacks {target.name} for {damage} points.'})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append({'message': f'{self.owner.name} attacks {target.name} but does no damage.'})

        return results
