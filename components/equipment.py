from components.equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, right_hand=None, left_hand=None ):
        self.right_hand = right_hand
        self.left_hand = left_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.right_hand and self.right_hand.equippable:
            bonus += self.right_hand.equippable.max_hp_bonus

        if self.left_hand and self.left_hand.equippable:
            bonus += self.left_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.right_hand and self.right_hand.equippable:
            bonus += self.right_hand.equippable.power_bonus

        if self.left_hand and self.left_hand.equippable:
            bonus += self.left_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.right_hand and self.right_hand.equippable:
            bonus += self.right_hand.equippable.defense_bonus

        if self.left_hand and self.left_hand.equippable:
            bonus += self.left_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.RIGHT_HAND:
            if self.right_hand == equippable_entity:
                self.right_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.right_hand:
                    results.append({'dequipped': self.right_hand})

                self.right_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.LEFT_HAND:
            if self.left_hand == equippable_entity:
                self.left_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.left_hand:
                    results.append({'dequipped': self.left_hand})

                self.left_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results