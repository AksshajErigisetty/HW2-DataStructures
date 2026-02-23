import csv

# NOTE :
# I did not use ChatGPT in this project.


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
        if input is None or len(input) == 0:
            return None

        ops = {"+", "-", "*", "/"}
        stack = []  

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

        # In a valid postfix expression, one tree remains
        if len(stack) != 1:
            raise ValueError("Invalid postfix expression")

        return stack.pop()

    # Problem 2.1: Prefix (pre-order): root, left, right
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

    # Problem 2.2: Infix (in-order) with parentheses
    # Requirement: parentheses must be included even for the outermost expression
    # and parentheses must be individual elements in the returned list.
    def infixNotationPrint(self, head: TreeNode) -> list:
        if head is None:
            return []

        operators = {"+", "-", "*", "/"}

        def build(node):
            # Leaf (operand)
            if node.left is None and node.right is None:
                return [str(node.val)]

            # Operator nodes should always have two children
            if str(node.val) not in operators or node.left is None or node.right is None:
                raise ValueError("wrong expression tree")

            left_part = build(node.left)
            right_part = build(node.right)

            return ["("] + left_part + [str(node.val)] + right_part + [")"]

        return build(head)

    # Problem 2.3: Postfix (post-order): left, right, root
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
    # Implement your stack using either an array or a list
    # (i.e., implement the functions based on the Stack ADT we covered in class)
    # You may use Python's list structure as the underlying storage.
    # While you can use .append() to add elements, please ensure the implementation strictly follows the logic we discussed in class
    # (e.g., manually managing the "top" of the stack
    
    # Use your own stack implementation to solve problem 3

    def __init__(self):
        # TODO: initialize the stack
        pass

    # Problem 3: Write code to evaluate a postfix expression using stack and return the integer value
    # Use stack which you implemented above for this problem

    # input -> a postfix expression string. E.g.: "5 1 2 + 4 * + 3 -"
    # see the examples of test entries in p3_eval_postfix.csv
    # output -> integer value after evaluating the string. Here: 14

    # integers are positive and negative
    # support basic operators: +, -, *, /
    # handle division by zero appropriately

    # DO NOT USE EVAL function for evaluating the expression

    def evaluatePostfix(exp: str) -> int:
        # TODO: implement this using your Stack class
        pass


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