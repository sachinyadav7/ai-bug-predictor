import re
import tree_sitter
from tree_sitter import Language, Parser
import hashlib
import os

class CodePreprocessor:
    def __init__(self, language='python'):
        self.language = language
        self.parser = self._setup_parser()
        
        # Mapping for identifier normalization
        self.var_counter = 0
        self.var_map = {}
        
    def _setup_parser(self):
        """Initialize tree-sitter parser"""
        try:
            if self.language == 'python':
                import tree_sitter_python
                LANGUAGE = Language(tree_sitter_python.language())
                parser = Parser(LANGUAGE)
            elif self.language == 'java':
                import tree_sitter_java
                LANGUAGE = Language(tree_sitter_java.language())
                parser = Parser(LANGUAGE)
            # Add other languages as needed
            else:
                # Fallback to manual load if bindings not found or language not standard
                # This part is kept for flexibility but improved
                lib_path = 'build/my-languages.so'
                if os.path.exists(lib_path):
                    LANGUAGE = Language(lib_path, self.language)
                    parser = Parser(LANGUAGE)
                else:
                    print(f"Warning: No parser found for {self.language}")
                    return Parser()
        except Exception as e:
            print(f"Error setting up parser for {self.language}: {e}")
            # Try newer API style just in case of version mismatch
            try:
                # Some newer versions might use different API
                pass
            except:
                pass
            return Parser()
                
        return parser
    
    def preprocess(self, code):
        """Full preprocessing pipeline"""
        code = self._remove_comments(code)
        code = self._normalize_whitespace(code)
        code = self._normalize_identifiers(code)
        code = self._truncate_lines(code)
        return code
    
    def _remove_comments(self, code):
        """Remove comments and docstrings"""
        if self.language == 'python':
            # Remove docstrings
            code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
            code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
            # Remove single-line comments
            code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        elif self.language in ['java', 'javascript', 'typescript', 'c', 'cpp']:
            # Remove /* */ comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
            # Remove // comments
            code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        return code
    
    def _normalize_whitespace(self, code):
        """Standardize indentation and newlines"""
        lines = code.split('\n')
        # Remove empty lines at start/end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        # Normalize to 4-space indentation
        normalized = []
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                spaces = ' ' * (indent // 4 * 4)
                normalized.append(spaces + stripped)
            else:
                normalized.append('')
        
        return '\n'.join(normalized)
    
    def _normalize_identifiers(self, code):
        """
        Normalize variable names to generic forms
        Preserves semantics while reducing vocabulary
        """
        if not self.parser.language:
             return code
             
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        
        # Collect all identifiers
        identifiers = []
        def traverse(node):
            if node.type in ['identifier', 'variable_name']:
                text = code[node.start_byte:node.end_byte]
                if not self._is_keyword(text):
                    identifiers.append((node.start_byte, node.end_byte, text))
            for child in node.children:
                traverse(child)
        
        traverse(root)
        
        # Replace with normalized names (in reverse to maintain positions)
        result = code
        for start, end, name in reversed(identifiers):
            normalized = self._get_normalized_name(name)
            result = result[:start] + normalized + result[end:]
        
        return result
    
    def _is_keyword(self, name):
        """Check if identifier is a language keyword"""
        keywords = {
            'python': {'self', 'cls', 'True', 'False', 'None', 'print', 'len'},
            'java': {'this', 'super', 'true', 'false', 'null', 'System', 'String'},
            'javascript': {'this', 'undefined', 'null', 'true', 'false', 'console'}
        }
        return name in keywords.get(self.language, set())
    
    def _get_normalized_name(self, name):
        """Map variable to normalized form (VAR_0, FUNC_1, etc.)"""
        # Determine type
        if name[0].isupper():
            prefix = 'CLS'  # Class
        elif name.startswith('__') and name.endswith('__'):
            prefix = 'DUNDER'  # Magic method
        elif name.startswith('_'):
            prefix = 'PRIV'  # Private
        elif name.isupper():
            prefix = 'CONST'  # Constant
        else:
            prefix = 'VAR'  # Variable
        
        # Consistent mapping using hash
        if name not in self.var_map:
            self.var_map[name] = f"{prefix}_{len(self.var_map)}"
        
        return self.var_map[name]
    
    def _truncate_lines(self, code, max_lines=100):
        """Truncate to maximum lines"""
        lines = code.split('\n')
        if len(lines) > max_lines:
            code = '\n'.join(lines[:max_lines])
        return code
    
    def extract_functions(self, code):
        """Extract individual functions/methods"""
        if not self.parser.language:
            # Fallback for when parser isn't working: treat whole file as one function
            # This is just so we can proceed without crasing if build/my-languages.so is missing
            return [{
                'name': 'unknown_file_scope',
                'code': self.preprocess(code),
                'hash': hashlib.md5(code.encode()).hexdigest()[:8],
                'start_line': 1,
                'end_line': len(code.split('\n'))
            }]

        tree = self.parser.parse(code.encode())
        root = tree.root_node
        
        functions = []
        
        def traverse(node):
            if node.type in ['function_definition', 'method_definition', 
                           'method_declaration', 'function_declaration']:
                func_text = code[node.start_byte:node.end_byte]
                func_name = self._extract_function_name(node, code)
                
                # Preprocess individual function
                processed = self.preprocess(func_text)
                
                functions.append({
                    'name': func_name,
                    'code': processed,
                    'hash': hashlib.md5(processed.encode()).hexdigest()[:8],
                    'start_line': node.start_point[0] + 1, # 1-indexed
                    'end_line': node.end_point[0] + 1
                })
            
            for child in node.children:
                traverse(child)
        
        traverse(root)
        # If no functions found, maybe return the whole code?
        if not functions:
             return [{
                'name': 'global_scope',
                'code': self.preprocess(code),
                'hash': hashlib.md5(code.encode()).hexdigest()[:8],
                'start_line': 1,
                'end_line': len(code.split('\n'))
            }]
            
        return functions
    
    def _extract_function_name(self, node, code):
        """Extract function name from AST node"""
        for child in node.children:
            if child.type == 'identifier':
                return code[child.start_byte:child.end_byte]
            # Handle different AST structures
            if child.type == 'name':
                return code[child.start_byte:child.end_byte]
        return 'unknown'
