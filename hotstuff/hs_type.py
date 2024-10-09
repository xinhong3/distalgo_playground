import unittest

def create_leaf(parent, v):
    parent_hash = parent.hash if parent else None
    return Node(parent, v, hash((parent_hash, v)))

class Node:
    def __init__(self, parent, command, hash):
        self.parent = parent
        self.command = command
        self.hash = hash
    
    def extends(self, node):
        # If node is None, consider this as extending from the genesis node
        if node is None:
            return True
        
        if node.hash == self.hash:
            return True

        # Compare the hashes to check if this node extends from the given node
        current_node = self
        while current_node is not None:
            if current_node.hash == node.hash:
                return True
            current_node = current_node.parent
        return False
    
    def __str__(self):
        current_node = self
        values = []
        
        while current_node is not None:
            cmd_str = f"({current_node.command})" if current_node.command is not None else "(None)"
            values.append(cmd_str)
            current_node = current_node.parent
        
        return " <- ".join(reversed(values))


class TestCreateLeaf(unittest.TestCase):
    def test_create_leaf_extends_parent(self):
        """Test that create_leaf correctly sets the parent and satisfies extends."""
        parent_node = create_leaf(None, 'v1')  # Genesis node
        leaf_node = create_leaf(parent_node, 'v2')
        
        # The leaf node should extend from the parent node
        self.assertTrue(leaf_node.extends(parent_node), "Leaf node should extend from its parent")
    
    def test_create_leaf_extends_none(self):
        """Test that a leaf node created with None parent satisfies extends(None)."""
        leaf_node = create_leaf(None, 'v1')
        
        # The leaf node should extend from None
        self.assertTrue(leaf_node.extends(None), "Leaf node should extend from None")

    def test_create_leaf_chain(self):
        """Test that create_leaf correctly creates a chain of nodes."""
        node1 = create_leaf(None, None)  # Genesis node
        node2 = create_leaf(node1, 'v2')
        node3 = create_leaf(node2, 'v3')

        # Check that each node extends its ancestor
        self.assertTrue(node2.extends(node1), "Node2 should extend from Node1")
        self.assertTrue(node3.extends(node1), "Node3 should extend from Node1")
        self.assertTrue(node3.extends(node2), "Node3 should extend from Node2")

if __name__ == '__main__':
    unittest.main()
