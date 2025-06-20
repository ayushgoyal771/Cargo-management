class Node:
    def __init__(self, object_id, bin_id):
        self.object_id = object_id
        self.bin_id = bin_id
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1  # New node is initially added at leaf


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

        

