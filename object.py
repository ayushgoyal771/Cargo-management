from enum import Enum


class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4


class Object:
    def __init__(self, object_id, size, color):
        self.object_id = object_id
        self.size = size
        self.color = color
        self.left = None 
        self.right = None  
        self.parent = None
        self.height = 1

    def set_left(self, node):
        self.left = node  
        if node is not None:
            node.parent = self

    def set_right(self, node):
        self.right = node
        if node is not None:
            node.parent = self

    def update_height(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)

    def balance_factor(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

