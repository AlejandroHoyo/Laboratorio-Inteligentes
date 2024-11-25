
from dataclasses import dataclass, field
from typing import Any
import heapq

def create_queue_element_cls(include_data):
    def wrapper_decorator(cls):
        if include_data:
            cls.data = field(compare=True)
        return dataclass(order=True)(cls)
    return wrapper_decorator

class PriorityQueue:
    """A priority queue implementation using heaps which is not thread safe"""

    def __init__(self, keys=None, compare_data=False):
        self.queue = []
        self.keys = keys if keys is not None else []

        @create_queue_element_cls(compare_data)
        class Wrapper:
            order_items: tuple
            data: Any = field(default=None)

        self.queue_item_cls = Wrapper

    def insert(self, item):
        order_items = tuple(fn(item) for fn in self.keys)
        queue_item = self.queue_item_cls(order_items, item)
        heapq.heappush(self.queue, queue_item)

    def remove(self):
        queue_item = heapq.heappop(self.queue)
        return queue_item.data

    def is_empty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.queue)
