from parsimonious.grammar import Grammar

grammar = Grammar(r"""
Selector = IndirectChild IndirectChild*
IndirectChild = DirectChild (" "+ DirectChild)* 
DirectChild = Attr (CHILDOP Attr)*
Attr = (Identifiers !(ValueOp / COMMA)) / (Identifiers ValueOp Identifiers)

Identifiers = (Identifier / String / Regex / Wildcard) (COMMA (Identifier / String / Regex / Wildcard))*

ValueOp = " "* ("!=" / "=") " "*
COMMA = " "* "," " "*
CHILDOP = " "* ">" " "*

Identifier = ~r"[A-Z][A-Z0-9_-]*"i
String = ~r'"(?:[^"\\]|\\.)*"' / ~r"'(?:[^'\\]|\\.)*'"
Regex = ~r"/(?:[^/\\]|\\.)*/\w*"
Wildcard = "*"
""")

def parse(text):
    return grammar.parse(text)

if __name__=="__main__":
    tests = [
        [
            'k=v',
            "identifier=identifier"
        ],
        [
            'k = v',
            "spaces"
        ],
        [
            'k=/v/i',
            "regex"
        ],
        [
            'k="v"',
            "quoted string"
        ],
        [
            'k=*',
            "wildcard"
        ],
        [
            'k!=v',
            "ne"
        ],
        [
            'k1,k2=v',
            "multiple keys"
        ],
        [
            'k1,k2=v1,v2',
            "multiple values"
        ],
        [
            'k',
            "key only"
        ],
        [
            'k1,k2',
            "multiple key only"
        ],
        [
            'k1=v1 > k2=v2',
            "direct child"
        ],
        [
            'k1 > k2',
            "direct child (key only)"
        ],
        [
            'k1 > k2 > k3',
            "direct child (key only)"
        ],
        [
            'k1 k2',
            "indirect child (key only)"
        ],
        [
            'k1 k2 k3',
            "indirect child (key only)"
        ],
        [
            'k1=v1 k2',
            "indirect child"
        ],
        [
            'k1 k2=v2',
            "indirect child"
        ],
        [
            'k1=v1 k2=v2',
            "indirect child(k=v)"
        ],
    ]
    for test, desc in tests:
        print(test)
        r = parse(test)
        print(r)