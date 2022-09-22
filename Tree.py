import json
import math


# Class to represent a tree or subtree for the hierarchy
class Tree(object):
    # Constructor method, which initialises the tree
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        self.weight = 0
        self.traversed = 1
        self.max_distance = 0
        if children is not None:
            for child in children:
                self.add_child(child)

    # Returns an object representation of the tree class in string format
    def __repr__(self):
        return self.name

    # Represents the contents of the class object as a string. In this case it prints the tree that branches
    # from the given node
    def __str__(self, level=0):
        ret = "\t" * level + f"{repr(self.name)} : {str(self.weight)} : {self.traversed}\n"
        if level == 0:
            ret = f"Max Distance: {self.max_distance}\n" + ret
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    # Adds a child node to the current tree, asserts that the instance of node is of type Tree
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    # Performs a pre-traversal search on the tree
    def pre_traverse(self, value, level=0):
        assert isinstance(value, str)
        if value == self.name or value in self.name or self.name in value:
            return level
        for child in self.children:
            ret = child.pre_traverse(value, level + 1)
            if ret != -1:
                return ret
        return -1

    # traverses a path and adds 1 to every node traversed
    def traverse_path_add_traversal_score(self, path):
        if self.name == path[0][0]:
            self.traversed += 1
            del path[0]
        if len(path) > 0:
            for child in self.children:
                if child.name == path[0][0]:
                    child.traverse_path_add_traversal_score(path)
                    break

    # Calculates the weights of the tree and all children
    def calculate_weights(self):
        # Traverse each node in the tree and calculate the weight of the node using the equation: w(n) = (t+logt) * log(t + 3/3)
        # Where n is the node and t is the number of times the node has been traversed
        self.weight = (self.traversed+math.log(self.traversed) * math.log(self.traversed + 3/3))
        if self.children:
            for child in self.children:
                child.calculate_weights()

    # Returns the longest path in the tree
    def largest_distance(self, level=0):
        if self.children:
            distances = []
            for child in self.children:
                if level == 0:
                    distances.append(child.largest_distance(level + 1))
                else:
                    distances.append(child.largest_distance(level+1) + self.weight)
            if level == 0:
                sorted_distances = sorted(distances, reverse=True)
                self.max_distance = sorted_distances[0] + sorted_distances[1] + self.weight
                return self.max_distance
            return max(distances)
        return self.weight


# Calculates the path from the given node to a node with a desired value
def path_to_node(root, path, k):
    assert isinstance(k, str)
    if root is None:
        return False

    # append the node value to path
    path.append((root.name, root.weight))
    # Check if node value == k
    if root.name == k:
        return True, path
    # Check if k is found in the node's children
    if root.children:
        for child in root.children:
            if path_to_node(child, path, k):
                return True, path
    # If not present in subtree rooted within root then remove root from the path and return False
    path.pop()
    return False


# Calculates the distance between two nodes, this is used to measure the distance between two entities within the hierarchy
def distance(root, ent1, ent2):
    if root:
        # Check if both ents are present in the tree. Else there is no route
        if root.pre_traverse(str(ent1)) != -1 and root.pre_traverse(str(ent2)) != -1:
            path1 = []
            path_to_node(root, path1, str(ent1))

            path2 = []
            path_to_node(root, path2, str(ent2))

            # Iterate through the paths to find the common path length
            i = 0
            while i < len(path1) and i < len(path2):
                if path1[i] != path2[i]:
                    break
                i += 1
            # Calculate the path length by deducting the intersecting path length or till lCA
            distance = 0
            j = 0
            while j < i:
                distance += path1[j][1]
                j += 1
            if i < len(path1):
                k = i
                while k < len(path1):
                    distance += path1[k][1]
                    k += 1
            if i < len(path2):
                l = i
                while l < len(path2):
                    distance += path2[l][1]
                    l += 1
            return distance
    return -1


def get_children(data, level=2):
    children = []
    if data is not None:
        for child in data:
            if isinstance(data, dict):
                children.append(Tree(child, get_children(data[child], level + 1)))
            elif isinstance(data, list):
                children.append(Tree(child, None))
            else:
                raise Exception("Type error in json")
    return children


def initialise_weights(tree, dataset):
    for document in dataset:
        for ent in document:
            path = path_to_node(tree, [], str(ent))
            if path:
                tree.traverse_path_add_traversal_score(path[1])
    tree.calculate_weights()
    return tree


def get_tree(name, json_string):
    info = json_string[name]
    return Tree(name, get_children(info))


# Converts the contents of hierarchy.json to a tree
def json_to_tree(tree_name, dataset=None):
    if tree_name in ["cyber_alias", "attack_technique", "company"]:
        data = json.load(open('higherarchy.json', 'r'))
        tree = initialise_weights(get_tree(tree_name, data), dataset)
        tree.largest_distance()
        return tree
    return None


