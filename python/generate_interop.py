#!/usr/bin/env python3

"""
Script to generate Python interop bindings from C# interop.cs file.
This script parses the C# interop.cs file and generates a Python equivalent
using ctypes to interface with the native library.
"""

import re
import os
import sys
from typing import List, Dict, Tuple, Set, Optional

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Default to the expected location in the repo
        input_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 "csharp", "uwapi", "interop.cs")
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Default output in the python package
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  "uwapi", "uw", "interop.py")
    
    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")
    
    with open(input_file, 'r') as f:
        cs_code = f.read()
    
    python_code = convert_cs_to_python(cs_code)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(python_code)
    
    print(f"Successfully generated {output_file}")

def convert_cs_to_python(cs_code: str) -> str:
    """Convert C# interop code to Python ctypes equivalent."""
    
    # Extract all enums
    enums = extract_enums(cs_code)
    
    # Extract all structs
    structs = extract_structs(cs_code)
    
    # Extract constants
    constants = extract_constants(cs_code)
    
    # Extract function declarations
    functions = extract_functions(cs_code)
    
    # Generate Python code
    python_code = generate_python_code(enums, structs, constants, functions, cs_code)
    
    return python_code

def extract_enums(cs_code: str) -> List[Dict]:
    """Extract enum declarations from C# code."""
    enums = []
    
    # Match both regular enums and flag enums
    enum_pattern = r'(?:public\s+enum|public\s+enum\s+class|\[Flags\]\s*public\s+enum)\s+(\w+)(?:\s*:\s*\w+)?\s*\{([^}]+)\}'
    
    matches = re.finditer(enum_pattern, cs_code, re.DOTALL)
    
    for match in matches:
        enum_name = match.group(1)
        enum_body = match.group(2)
        
        # Check if it's a flags enum
        is_flags = '[Flags]' in cs_code.splitlines()[max(0, cs_code.count('\n', 0, match.start()) - 2)]
        
        # Extract enum values
        values = []
        for line in enum_body.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            if '=' in line:
                name, value = [x.strip() for x in line.split('=', 1)]
                # Remove trailing comma and comments
                if ',' in value:
                    value = value.split(',', 1)[0].strip()
                if '//' in value:
                    value = value.split('//', 1)[0].strip()
            else:
                name = line.rstrip(',')
                value = None  # Will be auto-assigned
                
            if name and name != "":
                values.append((name, value))
        
        enums.append({
            'name': enum_name,
            'values': values,
            'is_flags': is_flags
        })
    
    return enums

def extract_structs(cs_code: str) -> List[Dict]:
    """Extract struct declarations from C# code."""
    structs = []
    
    # Match struct declarations
    struct_pattern = r'\[StructLayout\(.*?\)\]\s*public\s+struct\s+(\w+)\s*\{([^}]+)\}'
    
    matches = re.finditer(struct_pattern, cs_code, re.DOTALL)
    
    for match in matches:
        struct_name = match.group(1)
        struct_body = match.group(2)
        
        # Extract fields
        fields = []
        struct_lines = struct_body.strip().split('\n')
        
        i = 0
        while i < len(struct_lines):
            line = struct_lines[i].strip()
            if not line or line.startswith('//'):
                i += 1
                continue
            
            # Check for MarshalAs attribute
            array_size = None
            if line.startswith('[MarshalAs') and 'SizeConst' in line:
                size_match = re.search(r'SizeConst\s*=\s*(\d+)', line)
                if size_match:
                    array_size = int(size_match.group(1))
                i += 1
                if i >= len(struct_lines):
                    break
                line = struct_lines[i].strip()
            
            # Extract field type and name
            parts = line.split()
            if len(parts) >= 2:
                field_type = parts[0]
                field_name = parts[1].rstrip(';')
                
                # Handle array declarations
                array_match = re.search(r'(\w+)\s*\[\]', field_type)
                if array_match:
                    field_type = f"{array_match.group(1)}[]"
                
                fields.append({
                    'type': field_type,
                    'name': field_name,
                    'array_size': array_size
                })
            
            i += 1
        
        structs.append({
            'name': struct_name,
            'fields': fields
        })
    
    return structs

def extract_constants(cs_code: str) -> List[Tuple[str, str, str]]:
    """Extract constant declarations from C# code."""
    constants = []
    
    # Match public const declarations
    const_pattern = r'public\s+const\s+(\w+)\s+(\w+)\s*=\s*([^;]+);'
    
    matches = re.finditer(const_pattern, cs_code)
    
    for match in matches:
        const_type = match.group(1)
        const_name = match.group(2)
        const_value = match.group(3).strip()
        
        constants.append((const_type, const_name, const_value))
    
    return constants

def extract_functions(cs_code: str) -> List[Dict]:
    """Extract DllImport function declarations from C# code."""
    functions = []
    
    # Match DllImport function declarations
    func_pattern = r'\[DllImport\(.*?\)\]\s*(?:\[return:MarshalAs\(.*?\)\]\s*)?public\s+static\s+extern\s+(\w+)\s+(\w+)\((.*?)\);'
    
    matches = re.finditer(func_pattern, cs_code, re.DOTALL)
    
    for match in matches:
        return_type = match.group(1)
        func_name = match.group(2)
        params_str = match.group(3).strip()
        
        # Check if return type is marshaled as bool
        return_is_bool = False
        return_marshal_match = re.search(r'\[return:MarshalAs\(UnmanagedType.I1\)\]', 
                                         cs_code.splitlines()[max(0, cs_code.count('\n', 0, match.start()) - 2)])
        if return_marshal_match or return_type == 'bool':
            return_is_bool = True
        
        # Parse parameters
        params = []
        if params_str:
            for param in params_str.split(','):
                param = param.strip()
                if not param:
                    continue
                
                # Handle MarshalAs attribute
                marshal_match = re.search(r'\[MarshalAs\(.*?\)\]', param)
                if marshal_match:
                    param = param.replace(marshal_match.group(0), '').strip()
                
                param_parts = param.split()
                if len(param_parts) >= 2:
                    param_type = param_parts[0]
                    param_name = param_parts[1]
                    is_ref = 'ref' in param
                    is_bool = 'bool' in param_type or '[MarshalAs(UnmanagedType.I1)]' in param
                    is_string = 'string' in param_type or '[MarshalAs(UnmanagedType.LPStr)]' in param
                    
                    params.append({
                        'type': param_type,
                        'name': param_name,
                        'is_ref': is_ref,
                        'is_bool': is_bool,
                        'is_string': is_string
                    })
        
        functions.append({
            'name': func_name,
            'return_type': return_type,
            'params': params,
            'return_is_bool': return_is_bool
        })
    
    return functions

def cs_type_to_ctypes(cs_type: str, array_size: Optional[int] = None) -> str:
    """Convert C# type to Python ctypes type."""
    type_map = {
        'byte': 'ctypes.c_uint8',
        'sbyte': 'ctypes.c_int8',
        'short': 'ctypes.c_int16',
        'ushort': 'ctypes.c_uint16',
        'int': 'ctypes.c_int32',
        'uint': 'ctypes.c_uint32',
        'long': 'ctypes.c_int64',
        'ulong': 'ctypes.c_uint64',
        'float': 'ctypes.c_float',
        'double': 'ctypes.c_double',
        'bool': 'ctypes.c_bool',
        'char': 'ctypes.c_char',
        'IntPtr': 'ctypes.c_void_p',
        'void': 'None',
        'string': 'ctypes.c_char_p'
    }
    
    # Handle array types
    if array_size is not None:
        base_type = cs_type.rstrip('[]')
        ctypes_type = type_map.get(base_type, base_type)
        return f"{ctypes_type} * {array_size}"
    
    return type_map.get(cs_type, cs_type)

def generate_python_code(enums: List[Dict], structs: List[Dict], 
                         constants: List[Tuple[str, str, str]], 
                         functions: List[Dict], cs_code: str = "") -> str:
    """Generate Python code from parsed C# components."""
    
    code = []
    
    # Add file header
    code.append('#!/usr/bin/env python3')
    code.append('')
    code.append('# THIS FILE IS GENERATED BY SCRIPT')
    code.append('# DO NOT MODIFY')
    code.append('')
    code.append('import ctypes')
    code.append('import enum')
    code.append('import platform')
    code.append('from typing import Optional, List, Tuple, Callable, Any')
    code.append('')
    
    # Add library loading code
    code.append('# Determine which library to use based on platform')
    code.append('if platform.system() == "Windows":')
    code.append('    lib_ext = ".dll"')
    code.append('elif platform.system() == "Darwin":')
    code.append('    lib_ext = ".dylib"')
    code.append('else:')
    code.append('    lib_ext = ".so"')
    code.append('')
    code.append('# Use hardened library by default')
    code.append('HARDENED = True')
    code.append('if HARDENED:')
    code.append('    # hardened library contains additional checks to verify proper use of the api')
    code.append('    LIB_NAME = "unnatural-uwapi-hard"')
    code.append('else:')
    code.append('    # non-hard library may crash the program if used incorrectly')
    code.append('    LIB_NAME = "unnatural-uwapi"')
    code.append('')
    code.append('try:')
    code.append('    lib = ctypes.cdll.LoadLibrary(LIB_NAME + lib_ext)')
    code.append('except OSError:')
    code.append('    # Try to find the library in standard locations')
    code.append('    try:')
    code.append('        lib = ctypes.cdll.LoadLibrary(LIB_NAME)')
    code.append('    except OSError as e:')
    code.append('        raise ImportError(f"Could not load library {LIB_NAME}: {e}")')
    code.append('')
    
    # Add constants
    code.append('# Define constants')
    for const_type, const_name, const_value in constants:
        code.append(f'{const_name} = {const_value}')
    code.append('')
    
    # Add enums
    code.append('# Define enums')
    for enum in enums:
        enum_type = 'enum.IntFlag' if enum['is_flags'] else 'enum.IntEnum'
        code.append(f"class {enum['name']}({enum_type}):")
        
        # Handle None/None_ name clash in Python
        for i, (name, value) in enumerate(enum['values']):
            if name == 'None':
                name = 'None_'
            
            if value is None:
                # Auto-assign values starting from 0 if not specified
                if i == 0:
                    code.append(f"    {name} = 0")
                else:
                    prev_name, _ = enum['values'][i-1]
                    if prev_name == 'None':
                        prev_name = 'None_'
                    code.append(f"    {name} = {prev_name} + 1")
            else:
                code.append(f"    {name} = {value}")
        
        code.append('')
    
    # Add struct definitions
    code.append('# Define structures')
    for struct in structs:
        code.append(f"class {struct['name']}(ctypes.Structure):")
        code.append("    _fields_ = [")
        
        for field in struct['fields']:
            field_type = field['type']
            field_name = field['name']
            array_size = field['array_size']
            
            ctypes_type = cs_type_to_ctypes(field_type, array_size)
            code.append(f'        ("{field_name}", {ctypes_type}),')
        
        code.append("    ]")
        code.append("")
    
    # Add callback type definitions
    code.append('# Define callback types')
    for func in functions:
        if func['name'].startswith('uwSet') and len(func['params']) > 0:
            callback_param = func['params'][0]
            if 'Callback' in callback_param['type']:
                callback_name = callback_param['type']
                # Extract parameters from the callback delegate type
                callback_params = []
                callback_return = 'None'
                
                # Find the callback delegate definition
                delegate_pattern = r'public\s+delegate\s+(\w+)\s+' + re.escape(callback_name) + r'\s*\((.*?)\);'
                delegate_match = re.search(delegate_pattern, cs_code, re.DOTALL)
                
                if delegate_match:
                    return_type = delegate_match.group(1)
                    params_str = delegate_match.group(2).strip()
                    
                    callback_return = cs_type_to_ctypes(return_type)
                    
                    # Parse parameters
                    if params_str:
                        for param in params_str.split(','):
                            param = param.strip()
                            if not param:
                                continue
                            
                            # Handle MarshalAs attribute
                            if '[MarshalAs' in param:
                                if 'UnmanagedType.I1' in param:  # bool
                                    callback_params.append('ctypes.c_bool')
                                elif 'UnmanagedType.LPStr' in param:  # string
                                    callback_params.append('ctypes.c_char_p')
                                else:
                                    # Default to pointer type for complex marshaling
                                    callback_params.append('ctypes.c_void_p')
                                continue
                            
                            param_parts = param.split()
                            if len(param_parts) >= 2:
                                param_type = param_parts[0]
                                if 'ref' in param:
                                    # Reference parameters become pointers
                                    callback_params.append(f'ctypes.POINTER({cs_type_to_ctypes(param_type)})')
                                else:
                                    callback_params.append(cs_type_to_ctypes(param_type))
                
                params_str = ", ".join(callback_params) if callback_params else ""
                code.append(f"{callback_name} = ctypes.CFUNCTYPE({callback_return}, {params_str})")
    
    code.append('')
    
    # Add function prototypes
    code.append('# Define function prototypes')
    for func in functions:
        # Skip delegate definitions
        if 'delegate' in func['name'].lower():
            continue
            
        # Define argument types
        arg_types = []
        for param in func['params']:
            if param['is_ref']:
                struct_name = param['type'].replace('ref ', '')
                arg_types.append(f"ctypes.POINTER({struct_name})")
            elif param['is_string']:
                arg_types.append("ctypes.c_char_p")
            elif param['is_bool']:
                arg_types.append("ctypes.c_bool")
            else:
                arg_types.append(cs_type_to_ctypes(param['type']))
        
        args_str = ", ".join(arg_types) if arg_types else ""
        code.append(f"lib.{func['name']}.argtypes = [{args_str}]")
        
        # Define return type
        if func['return_is_bool']:
            code.append(f"lib.{func['name']}.restype = ctypes.c_bool")
        elif func['return_type'] == 'void':
            code.append(f"lib.{func['name']}.restype = None")
        else:
            code.append(f"lib.{func['name']}.restype = {cs_type_to_ctypes(func['return_type'])}")
    
    code.append('')
    
    # Add helper functions
    code.append('# Helper functions for string conversion')
    code.append('def to_bytes(s: str) -> bytes:')
    code.append('    return s.encode(\'utf-8\') if s is not None else None')
    code.append('')
    code.append('def from_bytes(b: bytes) -> str:')
    code.append('    return b.decode(\'utf-8\') if b is not None else None')
    code.append('')
    
    # Add array helper function
    code.append('# Helper functions for working with UwIds')
    code.append('def get_uint32_array(ptr: ctypes.c_void_p, count: int) -> List[int]:')
    code.append('    """Convert a C array of uint32 to a Python list."""')
    code.append('    if not ptr or count == 0:')
    code.append('        return []')
    code.append('    array_type = ctypes.c_uint32 * count')
    code.append('    return list(array_type.from_address(ptr))')
    code.append('')
    
    # Add Entity wrapper class
    code.append('# Entity class to wrap component fetching')
    code.append('class Entity:')
    code.append('    def __init__(self, entity_id: int):')
    code.append('        self.id = entity_id')
    code.append('        self.pointer = lib.uwEntityPointer(entity_id)')
    code.append('        self.components = {}')
    code.append('        ')
    code.append('    def fetch_components(self):')
    code.append('        """Fetch all available components for this entity."""')
    
    # Add component fetching based on structs
    component_structs = [s for s in structs if s['name'].endswith('Component')]
    for struct in component_structs:
        component_name = struct['name']
        snake_case_name = ''.join(['_'+c.lower() if c.isupper() else c for c in component_name[2:]]).lstrip('_')
        code.append(f'        self._try_fetch_component("{snake_case_name}", {component_name})')
    
    code.append('        return self')
    code.append('        ')
    code.append('    def _try_fetch_component(self, name: str, component_type):')
    code.append('        component = component_type()')
    code.append('        fetch_func = getattr(lib, f"uwFetch{component_type.__name__}")')
    code.append('        if fetch_func(self.pointer, ctypes.byref(component)):')
    code.append('            self.components[name] = component')
    code.append('        ')
    code.append('    def __getattr__(self, name):')
    code.append('        if name in self.components:')
    code.append('            return self.components[name]')
    code.append('        raise AttributeError(f"Entity has no component \'{name}\'")')
    code.append('')
    
    # Add wrapper functions for all the C functions
    code.append('# Function wrappers')
    for func in functions:
        # Skip delegate definitions
        if 'delegate' in func['name'].lower():
            continue
        
        # Get function name in snake_case (remove uw prefix)
        snake_case_name = ''.join(['_'+c.lower() if c.isupper() else c for c in func['name'][2:]]).lstrip('_')
        
        # Get parameter list
        params = []
        default_values = []
        for param in func['params']:
            param_name = param['name']
            if param['is_ref']:
                # Reference parameters aren't passed in Python
                continue
            
            # Add type annotation
            if param['is_bool']:
                param_type = 'bool'
            elif param['is_string']:
                param_type = 'str'
            elif 'uint' in param['type']:
                param_type = 'int'
            elif 'int' in param['type']:
                param_type = 'int'
            elif 'float' in param['type']:
                param_type = 'float'
            elif 'Callback' in param['type']:
                param_type = f"Callable"
            else:
                # Use the C# type name for complex types
                param_type = param['type']
            
            params.append(f"{param_name}: {param_type}")
            
            # Add default values for optional parameters
            if param_name.startswith('extra') or param_name == 'timeout':
                default_values.append(f"{param_name}=\"\"" if param_type == 'str' else f"{param_name}=0")
        
        # Add default version parameter
        if func['name'] == 'uwInitialize':
            params.append(f"version: int = UW_VERSION")
        
        # Add function declaration
        if default_values:
            params_str = ", ".join(params) + ", " + ", ".join(default_values)
        else:
            params_str = ", ".join(params)
        
        # Determine return type
        if func['return_is_bool'] or func['return_type'] == 'bool':
            return_type = 'bool'
        elif func['return_type'] == 'void':
            return_type = 'None'
        elif func['return_type'] == 'ulong' or func['return_type'] == 'uint':
            return_type = 'int'
        elif func['return_type'] == 'float':
            return_type = 'float'
        elif 'ref' in func['return_type']:
            # Handle reference return types
            return_type = func['return_type'].replace('ref ', '')
        else:
            return_type = func['return_type']
        
        code.append(f'def {snake_case_name}({params_str}) -> {return_type}:')
        
        # Add docstring
        code.append(f'    """{func["name"][2:]} wrapper."""')
        
        # Function body
        if 'Callback' in func['name']:
            # Special handling for callback functions
            callback_type = func['params'][0]['type']
            code.append(f'    def c_callback({", ".join([p["name"] for p in func["params"] if "Callback" not in p["type"]])}):')
            
            # Find parameters for the callback function
            delegate_pattern = r'public\s+delegate\s+(\w+)\s+' + re.escape(callback_type) + r'\s*\((.*?)\);'
            delegate_match = re.search(delegate_pattern, cs_code, re.DOTALL)
            
            if delegate_match:
                params_str = delegate_match.group(2).strip()
                callback_params = []
                
                # Parse parameters
                if params_str:
                    for param in params_str.split(','):
                        param = param.strip()
                        if not param:
                            continue
                        
                        # Extract parameter name
                        param_parts = param.split()
                        if len(param_parts) >= 2:
                            param_name = param_parts[-1]
                            # Convert reference parameters
                            if 'ref' in param:
                                callback_params.append(f"{param_name}.contents")
                            # Convert string parameters
                            elif 'string' in param or 'UnmanagedType.LPStr' in param:
                                callback_params.append(f"from_bytes({param_name})")
                            # Convert enum parameters
                            elif any(enum['name'] in param for enum in enums):
                                for enum in enums:
                                    if enum['name'] in param:
                                        callback_params.append(f"{enum['name']}({param_name})")
                                        break
                                else:
                                    callback_params.append(param_name)
                            else:
                                callback_params.append(param_name)
                
                callback_args = ", ".join(callback_params)
                code.append(f'        callback({callback_args})')
            else:
                # Fallback if we can't parse the delegate
                code.append('        callback()')
            
            code.append('    ')
            code.append(f'    cb = {callback_type}(c_callback)')
            code.append('    # Save the callback to prevent garbage collection')
            code.append(f'    {snake_case_name}.callback = cb')
            code.append(f'    lib.{func["name"]}(cb)')
        elif len(func['params']) == 0:
            # No parameters, just call the function
            if func['return_type'] == 'void':
                code.append(f'    lib.{func["name"]}()')
            else:
                code.append(f'    return lib.{func["name"]}()')
        else:
            # Build the function call
            args = []
            for param in func['params']:
                param_name = param['name']
                if param['is_ref']:
                    struct_name = param['type'].replace('ref ', '')
                    # Handle structs passed by reference
                    if any(s['name'] == struct_name for s in structs):
                        code.append(f'    {param_name} = {struct_name}()')
                        args.append(f'ctypes.byref({param_name})')
                elif param['is_string']:
                    args.append(f'to_bytes({param_name})')
                elif param['is_bool']:
                    args.append(param_name)
                else:
                    args.append(param_name)
            
            args_str = ", ".join(args)
            
            # Handle different return types
            if func['return_type'] == 'void':
                code.append(f'    lib.{func["name"]}({args_str})')
                
                # For functions that fill a struct, return it
                for param in func['params']:
                    if param['is_ref'] and param['name'] != 'data':
                        code.append(f'    return {param["name"]}')
            else:
                # Special handling for functions that return arrays via a struct
                for param in func['params']:
                    if param['is_ref'] and param['type'] == 'ref UwIds':
                        code.append(f'    {param["name"]} = UwIds()')
                        code.append(f'    lib.{func["name"]}({args_str})')
                        code.append(f'    return get_uint32_array({param["name"]}.ids, {param["name"]}.count)')
                        break
                else:
                    # Regular return handling
                    if func['return_is_bool'] or func['return_type'] == 'bool':
                        code.append(f'    return lib.{func["name"]}({args_str})')
                    elif func['return_type'] == 'ulong' or func['return_type'] == 'uint':
                        code.append(f'    return lib.{func["name"]}({args_str})')
                    elif func['return_type'] == 'float':
                        code.append(f'    return lib.{func["name"]}({args_str})')
                    else:
                        # Handle complex return types
                        if func['return_type'] == 'IntPtr' and 'Json' in func['name']:
                            code.append(f'    return from_bytes(lib.{func["name"]}({args_str}))')
                        else:
                            code.append(f'    return lib.{func["name"]}({args_str})')
        
        code.append('')
    
    return "\n".join(code)

if __name__ == "__main__":
    main()