from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import *

class AsaLexer(RegexLexer):
    name = 'Asa'
    aliases = ['asa']
    filenames = ['*.asa']
    mimetypes = ['text/x-asa']

    tokens = {
        'root': [
            # Single-line comments
            (r'//.*?$', Comment.Single),

            # Multi-line comments
            (r'/\*', Comment.Multiline, 'comment'),

            # Compiler directives - #import (handled specially to allow colon highlighting)
            (r'(#import)(\s+)', bygroups(Keyword.Namespace, Text), 'import_path'),

            # Other compiler directives - matches any #directive pattern
            (r'#[a-zA-Z_]\w*\b', Keyword.Namespace),

            # Operator overloading: operator<symbol> :: ... - MUST come before 'operator' keyword
            (r'(operator\s*[+\-*/%=<>!&|^~@$?]+)(\s*)(::)',
             bygroups(Operator, Text, Operator)),

            # Control flow keywords
            (words((
                'if', 'else', 'while', 'for', 'return', 'break', 'continue',
                'throw', 'test', 'match', 'finally', 'in', 'yield', 'where',
                'unsafe', 'try', 'await'
            ), suffix=r'\b'), Keyword),

            # Declaration/structure keywords
            (words((
                'struct', 'enum', 'module', 'operator', 'cast', 'create', 'destroy',
                'impl', 'let', 'macro', 'pub', 'use', 'mod', 'trait', 'extern',
                'union', 'as', 'box', 'dyn'
            ), suffix=r'\b'), Keyword.Type),

            # Storage keywords
            (words(('move', 'exact', 'ref', 'static', 'const'), suffix=r'\b'),
             Keyword.Declaration),

            # Built-in types
            (words((
                'int', 'int8', 'int16', 'int32', 'int64', 'int128',
                'uint', 'uint8', 'uint16', 'uint32', 'uint64', 'uint128',
                'char', 'uchar', 'bool', 'double', 'float', 'float32', 'float64',
                'half', 'string', 'function', 'any', 'list', 'array', 'iterator'
            ), suffix=r'\b'), Keyword.Type),

            # Boolean and special literals
            (r'\b(true|false)\b', Keyword.Constant),
            (r'\b(this|void|super)\b', Name.Builtin.Pseudo),

            # Function definitions: name :: type(...) or name :: (...)
            # This needs to come before the general :: operator
            (r'([a-zA-Z_]\w*)(\s*)(::)(\s*)([a-zA-Z_]\w*)(\s*)(\()',
             bygroups(Name.Function, Text, Operator, Text, Keyword.Type, Text, Punctuation)),
            (r'([a-zA-Z_]\w*)(\s*)(::)(\s*)(\()',
             bygroups(Name.Function, Text, Operator, Text, Punctuation)),

            # Function calls
            (r'([a-zA-Z_]\w*)(\s*)(\()',
             bygroups(Name.Function, Text, Punctuation)),

            # Type annotations: name : type or name : *type or name : const/ref/exact type
            (r'([a-zA-Z_]\w*)(\s*)(:)(\s*)(\*?)(\s*)((?:const|ref|exact)\s+)?(\*?)(\s*)([a-zA-Z_]\w*)',
             bygroups(Name.Variable, Text, Punctuation, Text, Operator, Text,
                     Keyword.Declaration, Operator, Text, Keyword.Type)),

            # Compile-time define operator ::
            (r'::', Operator),

            # Range operator
            (r'\.\.\.?', Operator),

            # Member access
            (r'\.', Punctuation),

            # Logical operators
            (r'(&&|\|\|)', Operator),

            # Comparison and arithmetic operators
            (r'(\+\+|--|<<|>>|<=|>=|==|!=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=)',
             Operator),
            (r'[-+*/%=<>!&|^~@]', Operator),

            # Pointer and reference operators
            (r'\*(?!=)', Operator),  # Pointer, not followed by =
            (r'&(?!=)', Operator),   # Reference, not followed by =

            # Arrow operator
            (r'->', Operator),

            # Question mark
            (r'\?', Operator),

            # Numbers - hexadecimal
            (r'0[xX][0-9a-fA-F_]+', Number.Hex),

            # Numbers - octal
            (r'0[oO][0-7_]+', Number.Oct),

            # Numbers - binary
            (r'0[bB][01_]+', Number.Bin),

            # Numbers - floating point
            (r'\d[\d_]*\.(?!\.)[\d_]*([eE][+-]?[\d_]+)?(f32|f64)?', Number.Float),
            (r'\d[\d_]*([eE][+-]?[\d_]+)(f32|f64)?', Number.Float),
            (r'\d[\d_]*\.(f32|f64)', Number.Float),

            # Numbers - integer
            (r'\d[\d_]*', Number.Integer),

            # Strings
            (r'b?"([^"\\]|\\.)*"', String),
            (r'br#+".*?"#+', String),  # Raw strings

            # Characters
            (r"b?'([^'\\]|\\.)+'", String.Char),

            # Punctuation
            (r'[{}()\[\];,]', Punctuation),

            # Identifiers
            (r'[a-zA-Z_]\w*', Name),

            # Whitespace
            (r'\s+', Text),
        ],

        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],

        'import_path': [
            # Module name component
            (r'[A-Za-z_][A-Za-z0-9_]*', Name.Namespace),
            # Colon separator
            (r':', Punctuation),
            # Asterisk for wildcard imports
            (r'\*', Operator),
            # Semicolon ends the import
            (r';', Punctuation, '#pop'),
            # Whitespace
            (r'\s+', Text),
        ]
    }
