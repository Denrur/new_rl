# import heapq
# from queue import PriorityQueue
from pqdict import pqdict
from entity import Entity


class PriorQueue:
    def __init__(self):
        self.queue = pqdict()

    def __len__(self):
        return len(self.queue)

    def keys(self):
        return self.queue.keys()

    def enqueue(self, value, priority=0.0):
        # tup = [priority, id(value), value]
        self.queue[value] = priority

    def adjust_priority(self, add):
        for v in self.queue:
            self.queue[v] += add

    def dequeue(self):
        return self.queue.pop()

    def dequeue_with_key(self):
        return self.queue.popitem()

    def erase(self, value):
        del self.queue[value]


class TimeSchedule:
    def __init__(self):
        self.scheduled_events = PriorQueue()

    def __len__(self):
        return len(self.scheduled_events)

    def keys(self):
        return self.scheduled_events.keys()

    def schedule_event(self, event, delay=0.0):
        if event is not None:
            self.scheduled_events.enqueue(event, delay)

    def next_event(self):

        event, time = self.scheduled_events.dequeue_with_key()
        self.scheduled_events.adjust_priority(-time)

        return event

    def cancel_event(self, event):

        self.scheduled_events.erase(event)


if __name__ == '__main__':
    from collections import defaultdict
    layer = defaultdict(tuple)
    a = Entity(name='Player', speed=75, energy=100, layer=layer)
    b = Entity(name='Robot', speed=50, energy=100, layer=layer)
    c = Entity(name='Zombie', speed=25, energy=100, layer=layer)
    entities = [a, b, c]
    q = TimeSchedule()
    for i in entities:
        i.action_cost = 40
        q.schedule_event(i, i.action_delay)

    while True:
        print(q.keys())
        entity = q.next_event()
        print(entity.name, entity.action_delay)
        q.schedule_event(entity, entity.action_delay)
