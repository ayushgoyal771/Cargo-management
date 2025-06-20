from bin import Bin, AVLManager, NewAvl
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bin_manager = AVLManager()
        self.new_tree = NewAvl()

    def add_bin(self, bin_id, capacity):
        self.bin_manager.insert(bin_id, capacity)

    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)

        # Find a suitable bin for the object
        suitable_bin = self._find_suitable_bin(obj)

        if suitable_bin is None:
            raise NoBinFoundException()

        # Add the object to the suitable bin
        self.new_tree.insert(object_id, suitable_bin.bin_id)
        self.bin_manager.add_object(suitable_bin, suitable_bin.bin_id, obj)

        # Update the bin's capacity
        old_capacity = suitable_bin.capacity
        new_capacity = old_capacity - obj.size

        # Preserve the current objects in the bin
        old_objects_tree = suitable_bin.objects_tree

        # Save the bin's id before deletion
        temp_id = suitable_bin.bin_id

        # Delete the bin from the trees
        self.bin_manager.delete(suitable_bin.bin_id)

        # Insert the bin with the updated capacity
        self.bin_manager.insert(temp_id, new_capacity)

        # Find the newly inserted bin and reassign the old objects
        new_bin = self.bin_manager.id_tree.search(self.bin_manager.id_tree.root, temp_id)

        if new_bin is None:
            raise NoBinFoundException()

        new_bin.objects_tree = old_objects_tree
        old_objects_tree = None

    def delete_object(self, object_id):
        newcurrent = self.new_tree.my_tree.search_object(self.new_tree.my_tree.root, object_id)
        newbin_id = newcurrent.bin_id
        new_bin = self.bin_manager.id_tree.search(self.bin_manager.id_tree.root, newbin_id)
        to_delete = new_bin.objects_tree.search_object(new_bin.objects_tree.root, object_id)
        old_objects_tree = new_bin.objects_tree
        temp_id = new_bin.bin_id
        add_capacity = new_bin.capacity + to_delete.size
        self.new_tree.delete(object_id)

        self.bin_manager.remove_object(newbin_id, object_id)
        self.bin_manager.delete(new_bin.bin_id)

        # Insert the bin with the updated capacity
        self.bin_manager.insert(temp_id, add_capacity)

        # Find the newly inserted bin and reassign the old objects
        mm_bin = self.bin_manager.id_tree.search(self.bin_manager.id_tree.root, temp_id)

        if mm_bin is None:
            raise NoBinFoundException()

        mm_bin.objects_tree = old_objects_tree
        old_objects_tree = None

    def object_info(self, object_id):
        newcurrent = self.new_tree.my_tree.search_object(self.new_tree.my_tree.root, object_id)

        # if not newcurrent:
        #     return None

        newbin_id = newcurrent.bin_id
        return newbin_id

    def bin_info(self, bin_id):
        bin_node = self.bin_manager.id_tree.search(self.bin_manager.id_tree.root, bin_id)

        if bin_node is None:
            print(f"Bin {bin_id} not found.")
            return None

        current_capacity = bin_node.capacity
        object_ids = bin_node.get_object_ids()  # Ensure you have a method to get the object IDs
        return current_capacity, object_ids

    def _find_suitable_bin(self, obj):
        if obj.color in [Color.BLUE, Color.YELLOW]:
            suitable_node = self._compact_fit(obj)
        else:  # Color.RED or Color.GREEN
            suitable_node = self._largest_fit(obj)
        return self._get_bin_from_node(suitable_node)

    def _compact_fit(self, obj):
        current = self.bin_manager.capacity_tree.root
        suitable_bin = None

        # Step 1: Find the minimum suitable bin based on capacity
        if obj.color == Color.BLUE:
            while current:
                if current.capacity >= obj.size:
                    if suitable_bin is None or current.capacity < suitable_bin.capacity or (
                        current.capacity == suitable_bin.capacity and current.bin_id < suitable_bin.bin_id
                    ):
                        suitable_bin = current
                    current = current.left
                else:
                    current = current.right

            if not suitable_bin:
                return None
            return suitable_bin

        elif obj.color == Color.YELLOW:
            while current:
                if current.capacity >= obj.size:
                    if suitable_bin is None or current.capacity < suitable_bin.capacity:
                        suitable_bin = current
                    current = current.left
                else:
                    current = current.right

            if not suitable_bin:
                return None

            current = suitable_bin.right
            while current:
                if current.capacity == suitable_bin.capacity:
                    suitable_bin = current
                    current = current.right
                else:
                    current = current.left

            return suitable_bin

    def _largest_fit(self, obj):
        current = self.bin_manager.capacity_tree.root
        suitable_bin = None

        # Step 1: Find the largest suitable bin based on capacity (rightmost node)
        while current.right:
            current = current.right

        if current.capacity < obj.size:
            return None

        if obj.color == Color.GREEN:
            return current

        elif obj.color == Color.RED:
            temp = self.bin_manager.capacity_tree.root

            while temp.capacity != current.capacity and temp != current:
                temp = temp.right

        suitable = temp

        if not temp.left:
            return temp

        temp = temp.left

        while temp:
            if temp.capacity == suitable.capacity:
                suitable = temp
                temp = temp.left
            else:
                temp = temp.right

        return suitable

    def _get_bin_from_node(self, node):
        if node:
            return self.bin_manager.id_tree.search(self.bin_manager.id_tree.root, node.bin_id)
        return None
