from node import Node
from object import Object

def compare_objects(obj1, obj2):
    """Comparison function for AVL tree, based on object ID."""
    if obj1.object_id > obj2.object_id:
        return 1
    elif obj1.object_id < obj2.object_id:
        return -1
    else:
        return 0  # Object IDs cannot be equal


# Comparison function to compare based on capacity (value1) and id (value2)
def comp_by_capacity(node_1, node_2):
    if node_1.capacity > node_2.capacity:
        return 1
    elif node_1.capacity < node_2.capacity:
        return -1
    else:  # If capacities are equal, compare ids
        if node_1.bin_id < node_2.bin_id:
            return -1
        elif node_1.bin_id > node_2.bin_id:
            return 1
        return 0  # ID cannot be equal based on your constraints

def comp_by_id(node_1, node_2):
    if node_1.bin_id < node_2.bin_id:
        return -1
    elif node_1.bin_id > node_2.bin_id:
        return 1
    return 0  # ID cannot be equal based on your constraints



class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def getheight(self, root):
        if root is None:
            return 0
        return root.height
    
    

    def rotate_left(self, z):
        y = z.right
        z.set_right(y.left)
        y.set_left(z)
        z.update_height()
        y.update_height()
        return y  # Return y to replace z

    def rotate_right(self, z):
        y = z.left
        z.set_left(y.right)
        y.set_right(z)
        z.update_height()
        y.update_height()
        return y

    def rebalance(self, node):
        node.update_height()
        balance = node.balance_factor()

        # Left heavy subtree
        if balance > 1:
            if node.left.balance_factor() < 0:  # Left-Right case
                node.set_left(self.rotate_left(node.left))
            return self.rotate_right(node)

        # Right heavy subtree
        if balance < -1:
            if node.right.balance_factor() > 0:  # Right-Left case
                node.set_right(self.rotate_right(node.right))
            return self.rotate_left(node)

        return node

    def _insert(self, current, new_node):
        if current is None:
            self.size += 1
            return new_node

        comparison = self.comparator(new_node, current)

        if comparison < 0:
            if current.left is None:
                current.set_left(new_node)
                self.size += 1
            else:
                current.set_left(self._insert(current.left, new_node))
        elif comparison > 0:
            if current.right is None:
                current.set_right(new_node)
                self.size += 1
            else:
                current.set_right(self._insert(current.right, new_node))
        else:
            # Handle duplicates based on ID
            # print(f"Duplicate node found: ({current.capacity}, {current.bin_id})")
            return current  # Prevent duplicate nodes

        # After insertion, rebalance the tree and update heights
        return self.rebalance(current)

         

    def insertion(self, node):
        self.root = self._insert(self.root, node)

    def search_node_capacity(self, current, node):
        """
        Search for a node based on capacity and ID (if capacities are the same).
        Uses the comparator comp_by_capacity to determine the traversal.
        """
        if current is None:
            return None  # Node not found
        
        comparison = comp_by_capacity(node, current)

        if comparison == 0:
            return current  # Node found with the same capacity and ID
        elif comparison < 0:
            return self.search_node_capacity(current.left, node)  # Traverse left
        else:
            return self.search_node_capacity(current.right, node)  # Traverse right

    # Search function based on ID only
    def search_node_id(self, current, node):
        """
        Search for a node based solely on the bin_id (ID).
        Uses the comparator comp_by_id to determine the traversal.
        """
        if current is None:
            return None  # Node not found
        
        comparison = comp_by_id(node, current)

        if comparison == 0:
            return current  # Node found with the same ID
        elif comparison < 0:
            return self.search_node_id(current.left, node)  # Traverse left
        else:
            return self.search_node_id(current.right, node)

    # Search function to find a node by ID
    def search(self, current, id):
        if current is None:
            return None
        if current.bin_id == id:
            return current
        elif id < current.bin_id:
            return self.search(current.left, id)
        else:
            return self.search(current.right, id)
        
    def search_object(self, current, id):
        if current is None:
            return None
        if current.object_id == id:
            return current
        elif id < current.object_id:
            return self.search_object(current.left, id)
        else:
            return self.search_object(current.right, id)



    def delete_newobject(self , object_id):
        node_to_delete = self.search_object(self.root, object_id)

        if node_to_delete:
            self.root = self._delete_newobject(self.root, node_to_delete)
        

    def _delete_newobject(self, current, node_to_delete):
        if current is None:
            return current

        comparison = self.comparator(node_to_delete, current)

        if comparison < 0:
            current.set_left(self._delete_newobject(current.left, node_to_delete))
        elif comparison > 0:
            current.set_right(self._delete_newobject(current.right, node_to_delete))
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            # Replace the node to delete with the leftmost node in the right subtree
            temp = self.leftmost(current.right)
            current.object_id, current.bin_id = temp.object_id, temp.bin_id
            current.set_right(self._delete_newobject(current.right, temp))

        return self.rebalance(current)

         
    def delete_object(self, object_to_delete):
        """Delete an object based on object_id or capacity"""
        # Step 1: Search for the node in the ID-based tree
        node_to_delete = self.search_object(self.root, object_to_delete.object_id)

        # If node found, proceed to delete
        if node_to_delete:
            self.root = self._delete_object(self.root, node_to_delete)
        

    def _delete_object(self, current, node_to_delete):
        if current is None:
            return current

        comparison = self.comparator(node_to_delete, current)

        if comparison < 0:
            current.set_left(self._delete_object(current.left, node_to_delete))
        elif comparison > 0:
            current.set_right(self._delete_object(current.right, node_to_delete))
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            # Replace the node to delete with the leftmost node in the right subtree
            temp = self.leftmost(current.right)
            current.size, current.object_id ,current.color = temp.size, temp.object_id,temp.color
            current.set_right(self._delete_object(current.right, temp))

        return self.rebalance(current)
    # Delete function
    def _delete(self, current, node_to_delete):
        if current is None:
            return current

        comparison = self.comparator(node_to_delete, current)

        if comparison < 0:
            current.set_left(self._delete(current.left, node_to_delete))
        elif comparison > 0:
            current.set_right(self._delete(current.right, node_to_delete))
        else:
            # Node to delete is found
            if current.left is None:
                self.size -= 1
                return current.right
            elif current.right is None:
                self.size -= 1
                return current.left

            # Node has two children, find inorder successor (leftmost in the right subtree)
            temp = self.leftmost(current.right)
            
            # Transfer the data from the inorder successor
            current.bin_id, current.capacity , current.objects_tree = temp.bin_id, temp.capacity , temp.objects_tree
            
            # Delete the inorder successor in the right subtree
            current.set_right(self._delete(current.right, temp))

        # Rebalance the tree after deletion
        return self.rebalance(current)

    def delete(self, node):
        self.root = self._delete(self.root, node)


    

    def leftmost(self, starting_node):
        current = starting_node
        while current.left is not None:
            current = current.left
        return current

    def rightmost(self, starting_node):
        current = starting_node
        while current.right is not None:
            current = current.right
        return current




