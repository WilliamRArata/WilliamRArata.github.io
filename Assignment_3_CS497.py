class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def sortedListToBST(head):
    if not head:
        return None
    
    # Find the middle element using slow and fast pointers
    slow = fast = head
    prev = None
    while fast and fast.next:
        fast = fast.next.next
        prev = slow
        slow = slow.next
    
    # Create root node
    root = TreeNode(slow.val)
    
    # Set left subtree
    if prev:
        prev.next = None
        root.left = sortedListToBST(head)
    
    # Set right subtree
    root.right = sortedListToBST(slow.next)
    
    return root

def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    
    root.left = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:], inorder[mid+1:])
    
    return root

def maxPathSum(root):
    max_sum = float('-inf')
    
    def max_gain(node):
        nonlocal max_sum
        if not node:
            return 0
        
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def largestValues(root):
    if not root:
        return []
    
    result = []
    level = [root]
    
    while level:
        next_level = []
        level_max = float('-inf')
        
        for node in level:
            level_max = max(level_max, node.val)
            
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
        
        result.append(level_max)
        level = next_level
    
    return result

def balanceBST(root):
    def inorder(node):
        return inorder(node.left) + [node.val] + inorder(node.right) if node else []
    
    def buildBST(vals):
        if not vals:
            return None
        mid = len(vals) // 2
        root = TreeNode(vals[mid])
        root.left = buildBST(vals[:mid])
        root.right = buildBST(vals[mid+1:])
        return root
    
    return buildBST(inorder(root))