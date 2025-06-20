from avl import AVLTree, compare_objects , comp_by_capacity , comp_by_id
from object import Object , Color
from node import Node 


class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity 
        self.height = 1 
        self.left = None
        self.right = None
        self.parent = None 
        self.objects_tree = AVLTree(compare_objects)  # Tree of objects by ID

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

    def add_object(self, obj):
        """Add an object to the AVL tree if there's enough capacity."""
        if obj.size > self.capacity :   
            return False  # Not enough space
        self.objects_tree.insertion(obj)  # Insert object based on ID
    
        

    def remove_object(self, object_id):
        """Remove an object by its object_id."""
        # Create a temporary Object with the given ID to search for it

        node_to_remove = self.objects_tree.search_object(self.objects_tree.root, object_id)

        if node_to_remove:
            self.objects_tree.delete_object(node_to_remove)
        
    

    def get_object_ids(self):
        """Get a list of all object IDs in the bin."""
        object_ids = []
        self._inorder_traversal(self.objects_tree.root, object_ids)
        return object_ids

    def _inorder_traversal(self, node, object_ids):
        """In-order traversal to collect object IDs."""
        if node:
            self._inorder_traversal(node.left, object_ids)
            object_ids.append(node.object_id)
            self._inorder_traversal(node.right, object_ids)

class AVLManager:
    def __init__(self):
        self.id_tree = AVLTree(comp_by_id)
        self.capacity_tree = AVLTree(comp_by_capacity)

    def insert_by_id(self, bin_id, capacity):
        new_node = Bin(bin_id, capacity)
        self.id_tree.insertion(new_node)

    # Separate insertion for Capacity Tree
    def insert_by_capacity(self, bin_id, capacity):
        new_node = Bin(bin_id , capacity)
        self.capacity_tree.insertion(new_node)

    # General insert method that inserts into both trees
    def insert(self, bin_id, capacity):
        self.insert_by_id(bin_id, capacity)
        self.insert_by_capacity(bin_id, capacity)

        
    def delete_by_id(self, bin_id):
        node_to_delete = self.id_tree.search(self.id_tree.root, bin_id)
        if node_to_delete:
            self.id_tree.delete(node_to_delete)

    # Separate deletion from Capacity Tree using the capacity to find the node
    def delete(self, bin_id):
        # Search for the node once in the id_tree and extract its capacity
        node_to_delete = self.id_tree.search(self.id_tree.root, bin_id)
        
        if node_to_delete:
            # Extract capacity from the node to use in capacity_tree deletion
            capacity = node_to_delete.capacity

            # Delete from both trees using the stored id and capacity
            self.delete_by_id(bin_id)
            self.delete_by_capacity(bin_id , capacity)

    def delete_by_capacity(self, bin_id  , capacity):
        # Create a temporary node with the same capacity and id
        temp_node =  Bin(bin_id , capacity)
        # Use this temporary node to find and delete the correct node in the capacity tree
        self.capacity_tree.delete(temp_node)



    def add_object(self,bin ,bin_id ,obj):
        
        bin_node1 = self.id_tree.search(self.id_tree.root, bin_id)
        bin_node1.add_object(obj) 
 

    def remove_object(self , bin_id , obj_id):

        bin_node1 = self.id_tree.search(self.id_tree.root, bin_id)
        bin_node1.remove_object(obj_id)



class NewAvl:
    def __init__(self):
        self.my_tree = AVLTree(compare_objects)


    def insert(self , object_id , bin_id):
        new_node = Node(object_id , bin_id)
        self.my_tree.insertion(new_node) 
    
    def delete(self , object_id):

        self.my_tree.delete_newobject(object_id) 


