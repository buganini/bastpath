from parsimonious.nodes import NodeVisitor
from parser import parse

class Entities(list):
    def __repr__(self):
        return f"{{{', '.join([x.__repr__() for x in self])}}}"

class Entity:
    def __init__(self, desc, re, negate):
        self.desc = desc
        self.re = re
        self.negate = negate

    def __repr__(self):
        neg = ["","!"][self.negate]
        desc = [self.desc,"*"][self.desc is None]
        return f"{neg}{desc}"

class Expr:
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    def __repr__(self):
        if self.op is None:
            return f"{self.a}"
        else:
            return f"{self.a}{self.op}{self.b}"

class XPathTransformer(NodeVisitor):
    PROMOTES = ["!"]

    def visit_Selector(self, node, visited_children):
        # print("!Selector", node, "=>", visited_children)
        ret = [visited_children[0]]
        for c in visited_children[1]:
            if c[0]:
                ret.append("//")
            else:
                ret.append("/")
            ret.append(c[1])
        return ret

    def visit_Attr(self, node, visited_children):
        # print("!Attr", node, "=>", visited_children)
        return visited_children

    def visit_AttrKey(self, node, visited_children):
        # print("!AttrKey", node, "=>", visited_children)
        return Expr(visited_children[0], None, None)

    def visit_AttrKeyValue(self, node, visited_children):
        # print("!AttrKeyValue", node, "=>", visited_children)
        return Expr(visited_children[0], visited_children[1], visited_children[2])

    def visit_CHILDOP(self, node, visited_children):
        return visited_children[0]

    def visit_DIROP(self, node, visited_children):
        return True

    def visit_INDIROP(self, node, visited_children):
        return False

    def visit_COMPARATOR(self, node, visited_children):
        return node.text

    def visit_Entities(self, node, visited_children):
        # print("!Entities", node, "=>", visited_children)
        ret = [visited_children[0]]
        for c in visited_children[1]:
            ret.append(c[1])
        return Entities(ret)

    def visit_COMMA(self, node, visited_children):
        return "COMMA"

    def visit_Entity(self, node, visited_children):
        # print("!Entity", node, "=>", visited_children)
        ret = visited_children[1][0]
        if visited_children[0] == "!":
            if ret.desc is None:
                raise ValueError("Cannot negate wildcard")
            ret.negate = True
        return ret

    def visit_Identifier(self, node, visited_children):
        # print("!Identifier", node)
        return Entity(node.text, False, False)

    def visit_NOT(self, node, visited_children):
        return "!"

    def visit_String(self, node, visited_children):
        return Entity(node.text.decode('string_escape'), False, False)

    def visit_Wildcard(self, node, visited_children):
        return Entity(None, False, False)

    def visit_Regex(self, node, visited_children):
        return Entity(node.text, True, False)

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        # return node
        if len(visited_children) == 1 and visited_children[0] in self.PROMOTES:
            return visited_children[0]
        return visited_children or node

class Bastpath:
    def __init__(self, selector):
        self.visitor = XPathTransformer()
        self.ast = parse(selector)

    def __str__(self):
        return self.ast.__str__()

    def toXPath(self):
        return self.visitor.visit(self.ast)

if __name__=="__main__":
    tests = [
        [
            "a",
            ""
        ],
        [
            "*",
            ""
        ],
        [
            "a=b",
            ""
        ],
        [
            "!a=b",
            ""
        ],
        [
            "a,b=c",
            ""
        ],
        [
            "a b c",
            ""
        ],
        [
            "a>b > c",
            ""
        ],
        [
            "a b>b,c,!d, e",
            ""
        ],
        [
            "a b=/x/",
            ""
        ],
    ]
    for sel, xpath in tests:
        b = Bastpath(sel)
        print(sel)
        print(b.toXPath())
        # for data, expected in tdata:
        #     r = b.check(data)
        #     print(r, expected)