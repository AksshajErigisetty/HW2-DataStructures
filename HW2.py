import csv

# NOTE :
# I did not use AI in this project. I refered to slides and notes I Prepared. 
# I also referred to the Data Structures — Python 3.14.3 documentation for the edge cases tester.
# No external sources were used; all ideas are my own or from course lecture slides.


# IMPORTANT NOTE:
# in class professor said that we can't change the tester so i made test cases for problem 4 in different file.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val     
        self.left = left
        self.right = right


class HomeWork2:
    # Problem 1: Construct an expression tree (Binary Tree) from a postfix expression
    # input -> list of strings (e.g., [3,4,+,2,*])
    # this is parsed from p1_construct_tree.csv (check it out for clarification)

    # there are no duplicate numeric values in the input
    # support basic operators: +, -, *, /

    # output -> the root node of the expression tree. Here: [*,+,2,3,4,None,None]
    # Tree Node with * as root node, the tree should be as follows
    #         *
    #        / \
    #       +   2
    #      / \
    #     3   4
    
    
    
    # The edge cases are working properly as empty input gives notree
    # at the end only 1 node should remain , otherwise invalid postfix
    def constructBinaryTree(self, input) -> TreeNode:
        # Firstly checking if it is empty and returning none.
        if input is None or len(input) == 0:
            return None
        
        # saving the operands in the ops and stck to save the trees nodes
        ops = {"+", "-", "*", "/"}
        stack = []  
        #So here we Go through each token in the postfix list and If token is an operator, 
        # we pop the two nodes and create a node then push to the new subtree but if lessthan 2, weget wrong operands as the output
        for token in input:
            token = token.strip()

            if token in ops:
                
                if len(stack) < 2:
                    raise ValueError("Wrong operands")

                right = stack.pop()
                left = stack.pop()

                newNode = TreeNode(token)
                newNode.left = left
                newNode.right = right
                stack.append(newNode)
            else:
               
                try:
                    float(token)
                except ValueError:
                    raise ValueError("Invalid token")

                node = TreeNode(token)
                stack.append(node)                

        
        if len(stack) != 1:
            raise ValueError("Invalid postfix expression")

        return stack.pop()

    # Problem 2.1: Use pre-order traversal (root, left, right) to generate prefix notation
    # return an array of elements of a prefix expression
    # expected output for the tree from problem 1 is [*,+,3,4,2]
    # you can see the examples in p2_traversals.csv
    
    
    # In prefix, we visit the root first, then left node, then right right node .
    # I used a helper recursive function to go through the tree.
    # The values are stored in a list and returned at the end. and also it checks if the tree is empty.
    def prefixNotationPrint(self, head: TreeNode) -> list:
        if head is None:
            return []

        result = []

        def preorder(node):
            if node is None:
                return
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)

        preorder(head)
        return result

    # Problem 2.2: Use in-order traversal (left, root, right) for infix notation with appropriate parentheses.
    # return an array of elements of an infix expression
    # expected output for the tree from problem 1 is [(,(,3,+,4,),*,2,)]
    # you can see the examples in p2_traversals.csv

    # don't forget to add parentheses to maintain correct sequence
    # even the outermost expression should be wrapped
    # treat parentheses as individual elements in the returned list (see output)
    
    
    
    # here we use Parentheses are added to keep the correct expression order
    # The result is stored as a list and returned.
    def infixNotationPrint(self, head: TreeNode) -> list:
        if head is None:
            return []

        operators = {"+", "-", "*", "/"}

        def build(node):
            
            if node.left is None and node.right is None:
                return [str(node.val)]

            # Operator nodes should always have two children
            if str(node.val) not in operators or node.left is None or node.right is None:
                raise ValueError("wrong expression tree")

            left_part = build(node.left)
            right_part = build(node.right)

            return ["("] + left_part + [str(node.val)] + right_part + [")"]

        return build(head)

    # Problem 2.3: Use post-order traversal (left, right, root) to generate postfix notation.
    # return an array of elements of a postfix expression
    # expected output for the tree from problem 1 is [3,4,+,2,*]
    # you can see the examples in p2_traversals.csv



    #in postfix node, we visit left,right and then the root.
    # i then used a recursive function to go through the tree
    # each node value is added to the list 
    #this gives the correct postflix order 
    

    def postfixNotationPrint(self, head: TreeNode) -> list:
        if head is None:
            return []

        result = []
        # I used a separate helper function for recursion instead of writing a function inside a function. 
        # The helper is used to traverse the tree in left, right, root order and store the result.

        def postorder(node):
            if node is None:
                return
            postorder(node.left)
            postorder(node.right)
            result.append(str(node.val))

        postorder(head)
        return result

# In here , Evaluate postfix expression using stack
# I split the expression by space and check each token.
# If it is a number, I push it to the stack.
# If it is an operator, I pop two numbers, perform the operation, and push the result back.
# It also checks for invalid input and division by zero.
# At the end, only one value should remain, which is the final answer.
class Stack:
    # Implement your stack using either an array or a list
    # (i.e., implement the functions based on the Stack ADT we covered in class)
    # You may use Python's list structure as the underlying storage.
    # While you can use .append() to add elements, please ensure the implementation strictly follows the logic we discussed in class
    # (e.g., manually managing the "top" of the stack
    
    # Use your own stack implementation to solve problem 3
    def __init__(self):
        self.data = []
        self.top = -1

    def isEmpty(self):
        return self.top == -1

    def push(self, x):
        self.data.append(x)
        self.top += 1

    def pop(self):
        if self.isEmpty():
            raise IndexError("pop from empty stack")
        value = self.data[self.top]
        self.data.pop()
        self.top -= 1
        return value

    def size(self):
        return self.top + 1
    
    
    # Problem 3: Write code to evaluate a postfix expression using stack and return the integer value
    # Use stack which you implemented above for this problem

    # input -> a postfix expression string. E.g.: "5 1 2 + 4 * + 3 -"
    # see the examples of test entries in p3_eval_postfix.csv
    # output -> integer value after evaluating the string. Here: 14

    # integers are positive and negative
    # support basic operators: +, -, *, /
    # handle division by zero appropriately

    # DO NOT USE EVAL function for evaluating the expression

    def evaluatePostfix(self, exp: str) -> int:
        if exp is None or exp.strip() == "":
            raise ValueError("Empty expression")



        ops = ["+", "-", "*", "/"]
        parts = exp.split()

        for t in parts:
        
            if t in ops:
                if self.size() < 2:
                    raise ValueError("Not enough numbers")
                num2 = self.pop()
                num1 = self.pop()
                if t == "+":
                    self.push(num1 + num2)
                elif t == "-":
                    self.push(num1 - num2)
                elif t == "*":
                    self.push(num1 * num2)
                else:  
                    if num2 == 0:
                        raise ZeroDivisionError("division by zero")
                    self.push(num1 / num2)
            else:
                try:
                    self.push(float(t))
                except:
                    raise ValueError("Invalid token")

    
        if self.size() != 1:
            raise ValueError("Invalid postfix expression")
        answer = self.pop()
        return int(round(answer))





# Main Function. Do not edit the code below
if __name__ == "__main__":
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)

        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")
            

        
            
            