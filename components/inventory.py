class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = list()
        self.targeting_item = None

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message'   : 'You cannot carry anymore. Your inventory is full'
                })
        else:
            results.append({
                'item_added': item,
                'message'   : f'You pick up the {item.name}!'
                })
            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = list()

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': f'{item_entity.name} cannot be used'})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}

                item_use_results = item_component.use_function(self.owner,
                                                               **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = list()
        if self.owner.equipment.right_hand == item or self.owner.equipment.left_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({
            'item_dropped': item,
            'message'     : f'You dropped the {item.name}'
            })

        return results