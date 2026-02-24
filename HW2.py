import csv

# NOTE :
# I did not use AI in this project. I refered to slides and notes. 
# No external sources were used; all ideas are my own or from course lecture slides.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # operator like '+' or operand like '3'
        self.left = left
        self.right = right


class HomeWork2:
    # Problem 1: Construct an expression tree from a postfix expression list
    # input example: ["3","4","+","2","*"]
    # output: root TreeNode

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

        # after processing all of them we get one node and that is the root.
        if len(stack) != 1:
            raise ValueError("Invalid postfix expression")

        return stack.pop()

    # Problem 2.1: 
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

    # Problem 2.2
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

    # Problem 2.3: Postfix traversal
    #in postfix node, we visit left,right and then the root.
    # i then used a recursive function to go through the tree
    # each node value is added to the list 
    #this gives the correct postflix order 
    

    def postfixNotationPrint(self, head: TreeNode) -> list:
        if head is None:
            return []

        result = []

        def postorder(node):
            if node is None:
                return
            postorder(node.left)
            postorder(node.right)
            result.append(str(node.val))

        postorder(head)
        return result


class Stack:
    # Stack ADT using a Python list, but we manually track 'top'
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

    # Problem 3: Evaluate a space-separated postfix expression string
    # Do NOT use eval(). Support +, -, *, /
    # Handle division by zero by raising ZeroDivisionError
    def evaluatePostfix(self, exp: str) -> int:
        if exp is None or exp.strip() == "":
            raise ValueError("Empty expression")



        ops = ["+", "-", "*", "/"]
        parts = exp.split()

        for t in parts:
        # if it is an operator, pop two numbers and do the math
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

    # at the end, we should have only one answer left
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