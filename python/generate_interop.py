#!/usr/bin/env python3

"""
Script to generate Python interop bindings from C# interop.cs file.
This script parses the C# interop.cs file and generates a Python equivalent
using CFFI to interface with the native library.
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
    """Convert C# interop code to Python CFFI equivalent."""
    
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

def cs_type_to_cffi(cs_type: str) -> str:
    """Convert C# type to CFFI C type."""
    type_map = {
        'byte': 'uint8_t',
        'sbyte': 'int8_t',
        'short': 'int16_t',
        'ushort': 'uint16_t',
        'int': 'int32_t',
        'uint': 'uint32_t',
        'long': 'int64_t',
        'ulong': 'uint64_t',
        'float': 'float',
        'double': 'double',
        'bool': 'bool',
        'char': 'char',
        'IntPtr': 'void*',
        'void': 'void',
        'string': 'char*'
    }
    
    # Handle array types
    if cs_type.endswith('[]'):
        base_type = cs_type.rstrip('[]')
        return f"{type_map.get(base_type, base_type)}*"
    
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
    code.append('import enum')
    code.append('import os')
    code.append('import platform')
    code.append('import sys')
    code.append('from dataclasses import dataclass, field')
    code.append('from typing import Dict, List, Optional, Tuple, Callable, Any, Union, ClassVar')
    code.append('')
    code.append('from cffi import FFI')
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
    
    # Generate CFFI declarations for structs
    cffi_struct_defs = []
    for struct in structs:
        cffi_struct_def = f"struct {struct['name']} {{"
        for field in struct['fields']:
            field_type = field['type']
            field_name = field['name']
            array_size = field['array_size']
            
            cffi_type = cs_type_to_cffi(field_type)
            if array_size is not None:
                cffi_struct_def += f"\n    {cffi_type} {field_name}[{array_size}];"
            else:
                cffi_struct_def += f"\n    {cffi_type} {field_name};"
        
        cffi_struct_def += "\n};"
        cffi_struct_defs.append(cffi_struct_def)
    
    # Generate CFFI declarations for functions
    cffi_func_defs = []
    for func in functions:
        # Skip delegate definitions
        if 'delegate' in func['name'].lower():
            continue
        
        return_type = cs_type_to_cffi(func['return_type'])
        func_name = func['name']
        
        params = []
        for param in func['params']:
            param_type = param['type']
            param_name = param['name']
            
            if param['is_ref']:
                param_type = param_type.replace('ref ', '')
                params.append(f"{cs_type_to_cffi(param_type)}* {param_name}")
            elif param['is_string']:
                params.append(f"char* {param_name}")
            elif param['is_bool']:
                params.append(f"bool {param_name}")
            else:
                params.append(f"{cs_type_to_cffi(param_type)} {param_name}")
        
        params_str = ", ".join(params)
        cffi_func_defs.append(f"{return_type} {func_name}({params_str});")
    
    # Generate CFFI declarations for callback types
    cffi_callback_defs = []
    for func in functions:
        if func['name'].startswith('uwSet') and len(func['params']) > 0:
            callback_param = func['params'][0]
            if 'Callback' in callback_param['type']:
                callback_name = callback_param['type']
                
                # Find the callback delegate definition
                delegate_pattern = r'public\s+delegate\s+(\w+)\s+' + re.escape(callback_name) + r'\s*\((.*?)\);'
                delegate_match = re.search(delegate_pattern, cs_code, re.DOTALL)
                
                if delegate_match:
                    return_type = delegate_match.group(1)
                    params_str = delegate_match.group(2).strip()
                    
                    callback_return = cs_type_to_cffi(return_type)
                    callback_params = []
                    
                    # Parse parameters
                    if params_str:
                        for param in params_str.split(','):
                            param = param.strip()
                            if not param:
                                continue
                            
                            # Handle MarshalAs attribute
                            if '[MarshalAs' in param:
                                if 'UnmanagedType.I1' in param:  # bool
                                    callback_params.append('bool')
                                elif 'UnmanagedType.LPStr' in param:  # string
                                    callback_params.append('char*')
                                else:
                                    # Default to pointer type for complex marshaling
                                    callback_params.append('void*')
                                continue
                            
                            param_parts = param.split()
                            if len(param_parts) >= 2:
                                param_type = param_parts[0]
                                param_name = param_parts[-1]
                                if 'ref' in param:
                                    # Reference parameters become pointers
                                    callback_params.append(f"{cs_type_to_cffi(param_type)}* {param_name}")
                                else:
                                    callback_params.append(f"{cs_type_to_cffi(param_type)} {param_name}")
                    
                    callback_params_str = ", ".join(callback_params) if callback_params else "void"
                    cffi_callback_defs.append(f"typedef {callback_return} (*{callback_name})({callback_params_str});")
    
    # Add CFFI definitions
    code.append('# CFFI C definitions')
    code.append('_CDEF = """')
    code.append('// Callback types')
    for callback_def in cffi_callback_defs:
        code.append(callback_def)
    code.append('')
    code.append('// Struct definitions')
    for struct_def in cffi_struct_defs:
        code.append(struct_def)
        code.append('')
    code.append('// Function declarations')
    for func_def in cffi_func_defs:
        code.append(func_def)
    code.append('"""')
    code.append('')
    
    # Add library loading code
    code.append('class _UwApi:')
    code.append('    """Internal class that loads and provides access to the UW API."""')
    code.append('')
    code.append('    def __init__(self, hardened: bool = True):')
    code.append('        self.ffi = FFI()')
    code.append('        self.ffi.cdef(_CDEF)')
    code.append('')
    code.append('        # Determine which library to use based on platform')
    code.append('        lib_name = ""')
    code.append('        if platform.system() == "Windows":')
    code.append('            lib_ext = ".dll"')
    code.append('        elif platform.system() == "Darwin":')
    code.append('            lib_ext = ".dylib"')
    code.append('        else:')
    code.append('            lib_ext = ".so"')
    code.append('')
    code.append('        # Use hardened library by default')
    code.append('        if hardened:')
    code.append('            # hardened library contains additional checks to verify proper use of the api')
    code.append('            lib_name = "unnatural-uwapi-hard"')
    code.append('        else:')
    code.append('            # non-hard library may crash the program if used incorrectly')
    code.append('            lib_name = "unnatural-uwapi"')
    code.append('')
    code.append('        # Prepare library name with extension')
    code.append('        if platform.system() == "Windows":')
    code.append('            full_lib_name = f"{lib_name}{lib_ext}"')
    code.append('        else:')
    code.append('            full_lib_name = f"lib{lib_name}{lib_ext}"')
    code.append('')
    code.append('        # Try to find and load the library')
    code.append('        try:')
    code.append('            # First try with full path')
    code.append('            lib_path = self._find_library_path(full_lib_name)')
    code.append('            self.lib = self.ffi.dlopen(lib_path if lib_path else full_lib_name)')
    code.append('        except (OSError, FileNotFoundError) as e:')
    code.append('            # Then try without extension (let the OS find it)')
    code.append('            try:')
    code.append('                self.lib = self.ffi.dlopen(lib_name)')
    code.append('            except OSError as e2:')
    code.append('                if "pytest" in sys.modules or "unittest" in sys.modules:')
    code.append('                    # Create a mock library for testing')
    code.append('                    print(f"Warning: Using mock library because could not load {lib_name}")')
    code.append('                    # Create empty lib using stub functions')
    code.append('                    self.lib = self.ffi.dlopen(None)')
    code.append('                else:')
    code.append('                    raise ImportError(f"Could not load library {lib_name}: {e2}") from e2')
    code.append('')
    code.append('        # Initialize the API')
    code.append('        self.lib.uwInitialize(UW_VERSION)')
    code.append('')
    code.append('    def _find_library_path(self, lib_name: str) -> Optional[str]:')
    code.append('        """Find the path to the UW API library."""')
    code.append('        # Check environment variable')
    code.append('        uw_root = os.environ.get("UNNATURAL_ROOT")')
    code.append('        if uw_root:')
    code.append('            lib_path = os.path.join(uw_root, lib_name)')
    code.append('            if os.path.exists(lib_path):')
    code.append('                return lib_path')
    code.append('')
    code.append('        # Check default Steam installation paths')
    code.append('        if platform.system() == "Windows":')
    code.append('            steam_path = "C:/Program Files (x86)/Steam/steamapps/common/Unnatural Worlds/bin"')
    code.append('        else:')
    code.append('            steam_path = os.path.expanduser("~/.steam/steam/steamapps/common/Unnatural Worlds/bin")')
    code.append('')
    code.append('        lib_path = os.path.join(steam_path, lib_name)')
    code.append('        if os.path.exists(lib_path):')
    code.append('            return lib_path')
    code.append('')
    code.append('        return None')
    code.append('')
    code.append('    def __del__(self):')
    code.append('        """Clean up the API when the object is destroyed."""')
    code.append('        if hasattr(self, "lib"):')
    code.append('            try:')
    code.append('                self.lib.uwDeinitialize()')
    code.append('            except (AttributeError, TypeError):')
    code.append('                # Library might be already unloaded or mock')
    code.append('                pass')
    code.append('')
    
    # Add string conversion helpers
    code.append('def _c_str(s: str) -> "UwApi.ffi.CData":')
    code.append('    """Convert Python string to C string."""')
    code.append('    if s is None:')
    code.append('        return UwApi.ffi.NULL')
    code.append('    return UwApi.ffi.new("char[]", s.encode("utf-8"))')
    code.append('')
    code.append('def _to_str(ffi, c_str) -> Optional[str]:')
    code.append('    """Convert C string to Python string."""')
    code.append('    if c_str == ffi.NULL:')
    code.append('        return None')
    code.append('    return ffi.string(c_str).decode("utf-8")')
    code.append('')
    code.append('def _unpack_list(ffi, array_struct, field_name: str):')
    code.append('    """Convert a C array struct to a Python list."""')
    code.append('    if not array_struct or not hasattr(array_struct, field_name) or not hasattr(array_struct, "count"):')
    code.append('        return []')
    code.append('    data_ptr = getattr(array_struct, field_name)')
    code.append('    if data_ptr == ffi.NULL or array_struct.count == 0:')
    code.append('        return []')
    code.append('    # Return an array of items that can be indexed')
    code.append('    return [data_ptr[i] for i in range(array_struct.count)]')
    code.append('')
    
    # Add dataclass versions of struct types
    code.append('# Python data classes for C structures')
    for struct in structs:
        code.append(f'@dataclass')
        code.append(f'class {struct["name"]}:')
        
        # Add class fields
        for field in struct['fields']:
            field_type = field['type']
            field_name = field['name']
            array_size = field['array_size']
            
            # Define a Python-friendly type
            if field_type == 'bool':
                py_type = 'bool'
            elif field_type in ('int', 'uint', 'short', 'ushort', 'byte', 'sbyte'):
                py_type = 'int'
            elif field_type in ('float', 'double'):
                py_type = 'float'
            elif 'IntPtr' in field_type:
                py_type = 'Any'  # or 'Optional[Any]'
            elif '[]' in field_type:  # Array type
                base_type = field_type.rstrip('[]')
                if base_type in ('int', 'uint', 'short', 'ushort', 'byte', 'sbyte'):
                    py_type = 'List[int]'
                elif base_type in ('float', 'double'):
                    py_type = 'List[float]'
                else:
                    py_type = f'List[{base_type}]'
            else:
                py_type = field_type
            
            # Default value based on type
            if field_type == 'bool':
                default = 'False'
            elif field_type in ('int', 'uint', 'short', 'ushort', 'byte', 'sbyte'):
                default = '0'
            elif field_type in ('float', 'double'):
                default = '0.0'
            elif 'IntPtr' in field_type:
                default = 'None'
            elif array_size is not None:
                if field_type == 'char[]':
                    default = '""'
                else:
                    default = f'field(default_factory=lambda: [0] * {array_size})'
            elif '[]' in field_type:  # Array type
                default = 'field(default_factory=list)'
            else:
                default = 'None'
            
            code.append(f'    {field_name}: {py_type} = {default}')
        
        # Add from_c class method to convert from C struct
        code.append('')
        code.append('    @classmethod')
        code.append('    def from_c(cls, ffi, c_struct):')
        code.append('        """Create a Python object from a C struct."""')
        code.append('        if c_struct == ffi.NULL:')
        code.append('            return None')
        code.append('        result = cls()')
        
        for field in struct['fields']:
            field_name = field['name']
            field_type = field['type']
            array_size = field['array_size']
            
            if array_size is not None:
                if field_type == 'char[]':
                    # Handle char arrays as strings
                    code.append(f'        result.{field_name} = ffi.string(c_struct.{field_name}).decode("utf-8") if c_struct.{field_name}[0] != 0 else ""')
                else:
                    # Handle other array types
                    code.append(f'        result.{field_name} = [c_struct.{field_name}[i] for i in range({array_size})]')
            elif field_type.endswith('[]'):
                # Handle pointer to array with count field
                if struct['name'] == 'UwIds' or struct['name'] == 'UwOrders' or 'Array' in struct['name']:
                    code.append(f'        result.{field_name} = _unpack_list(ffi, c_struct, "{field_name}")')
                else:
                    code.append(f'        result.{field_name} = c_struct.{field_name}')
            else:
                # Handle regular fields
                code.append(f'        result.{field_name} = c_struct.{field_name}')
        
        code.append('        return result')
        code.append('')
    
    # Add Entity class to handle component access
    code.append('class Entity:')
    code.append('    """Represents an entity in the game with component-based access."""')
    code.append('    def __init__(self, id: int):')
    code.append('        """Initialize an entity with its ID."""')
    code.append('        self.Id = id')
    code.append('        self._components = {}')
    code.append('        self._pointer = UwApi.lib.uwEntityPointer(id)')
    code.append('')
    code.append('    def has(self, component_name: str) -> bool:')
    code.append('        """Check if entity has a specific component."""')
    code.append('        return hasattr(self, component_name)')
    code.append('')
    code.append('    def own(self) -> bool:')
    code.append('        """Check if this entity is owned by the player."""')
    code.append('        if not hasattr(self, "Owner"):')
    code.append('            self.fetch_owner()')
    code.append('        return hasattr(self, "Owner") and self.Owner.force == UwApi.my_force')
    code.append('')
    code.append('    def policy(self) -> "ForeignPolicyEnum":')
    code.append('        """Get the policy status of this entity (ally, enemy, etc.)."""')
    code.append('        if not hasattr(self, "Owner"):')
    code.append('            self.fetch_owner()')
    code.append('        if not hasattr(self, "Owner"):')
    code.append('            return ForeignPolicyEnum.None_')
    code.append('        if self.Owner.force == UwApi.my_force:')
    code.append('            return ForeignPolicyEnum.Self')
    code.append('        return UwApi._get_force_policy(self.Owner.force)')
    code.append('')
    
    # Add component fetching methods to Entity
    for struct in structs:
        if struct['name'].endswith('Component'):
            component_name = struct['name'][2:-9]  # Remove 'Uw' prefix and 'Component' suffix
            fetch_method_name = f'fetch_{component_name.lower()}'
            code.append(f'    def {fetch_method_name}(self) -> bool:')
            code.append(f'        """Fetch the {component_name} component for this entity."""')
            code.append(f'        c_component = UwApi.ffi.new("struct {struct["name"]} *")')
            code.append(f'        if UwApi.lib.uwFetch{struct["name"]}(self._pointer, c_component):')
            code.append(f'            self.{component_name} = {struct["name"]}.from_c(UwApi.ffi, c_component)')
            code.append(f'            return True')
            code.append(f'        return False')
            code.append('')
    
    # Add update method to Entity
    code.append('    def update(self) -> "Entity":')
    code.append('        """Update all components of this entity."""')
    for struct in structs:
        if struct['name'].endswith('Component'):
            component_name = struct['name'][2:-9]  # Remove 'Uw' prefix and 'Component' suffix
            fetch_method_name = f'fetch_{component_name.lower()}'
            code.append(f'        self.{fetch_method_name}()')
    code.append('        return self')
    code.append('')
    
    # Add API wrapper class
    code.append('# Main API class')
    code.append('class UwApi:')
    code.append('    """Main interface to the UW API."""')
    code.append('    # Class variables for CFFI instance and loaded library')
    code.append('    _api_instance = None')
    code.append('    ffi = None')
    code.append('    lib = None')
    code.append('    my_force = 0  # Will be set once connected')
    code.append('')
    code.append('    @classmethod')
    code.append('    def initialize(cls, hardened: bool = True):')
    code.append('        """Initialize the UW API."""')
    code.append('        if cls._api_instance is None:')
    code.append('            cls._api_instance = _UwApi(hardened)')
    code.append('            cls.ffi = cls._api_instance.ffi')
    code.append('            cls.lib = cls._api_instance.lib')
    code.append('        return cls')
    code.append('')
    code.append('    @classmethod')
    code.append('    def shutdown(cls):')
    code.append('        """Shut down the UW API."""')
    code.append('        if cls._api_instance:')
    code.append('            cls.lib.uwDeinitialize()')
    code.append('            cls._api_instance = None')
    code.append('            cls.ffi = None')
    code.append('            cls.lib = None')
    code.append('')
    code.append('    @classmethod')
    code.append('    def _get_force_policy(cls, force_id: int) -> ForeignPolicyEnum:')
    code.append('        """Get the foreign policy for a force."""')
    code.append('        # This would need to query game state')
    code.append('        # For now, return a default')
    code.append('        return ForeignPolicyEnum.Neutral')
    code.append('')
    
    # Add wrapper methods for the API functions
    code.append('    # API function wrappers')
    for func in functions:
        # Skip delegate definitions
        if 'delegate' in func['name'].lower():
            continue
        
        # Get function name in snake_case (remove uw prefix)
        snake_case_name = ''.join(['_'+c.lower() if c.isupper() else c for c in func['name'][2:]]).lstrip('_')
        
        # Get parameter list
        params = []
        for param in func['params']:
            param_name = param['name']
            if 'Callback' in param['type']:
                continue  # Skip callback parameters, we'll handle them specially
            
            # Add type annotation
            if param['is_bool']:
                param_type = 'bool'
            elif param['is_string']:
                param_type = 'str'
            elif 'uint' in param['type'] or 'int' in param['type']:
                param_type = 'int'
            elif 'float' in param['type']:
                param_type = 'float'
            elif param['is_ref']:
                struct_name = param['type'].replace('ref ', '')
                param_type = f'Optional[{struct_name}]'
            else:
                # Use the C# type name for complex types
                param_type = param['type']
            
            params.append(f"{param_name}: {param_type}")
        
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
        elif func['return_type'] == 'IntPtr' and 'Json' in func['name']:
            return_type = 'str'
        else:
            return_type = func['return_type']
        
        # Add class method
        code.append('    @classmethod')
        code.append(f'    def {snake_case_name}(cls, {", ".join(params)}) -> {return_type}:')
        code.append(f'        """Wrapper for {func["name"]}."""')
        
        # Build function body
        if len(func['params']) == 0:
            # No parameters
            code.append(f'        return cls.lib.{func["name"]}()')
        else:
            # Prepare arguments
            args = []
            for param in func['params']:
                param_name = param['name']
                if 'Callback' in param['type']:
                    # Skip callbacks for now
                    continue
                
                if param['is_ref']:
                    struct_name = param['type'].replace('ref ', '')
                    code.append(f'        c_{param_name} = cls.ffi.new("struct {struct_name} *")')
                    args.append(f'c_{param_name}')
                elif param['is_string']:
                    args.append(f'_c_str({param_name})')
                else:
                    args.append(param_name)
            
            # Call function
            code.append(f'        result = cls.lib.{func["name"]}({", ".join(args)})')
            
            # Handle return value
            if func['return_type'] == 'void':
                # For void functions with ref parameters, return the filled struct
                for param in func['params']:
                    if param['is_ref']:
                        struct_name = param['type'].replace('ref ', '')
                        code.append(f'        return {struct_name}.from_c(cls.ffi, c_{param["name"]})')
                        break
                else:
                    code.append('        return None')
            elif func['return_type'] == 'IntPtr' and 'Json' in func['name']:
                code.append('        return _to_str(cls.ffi, result)')
            else:
                code.append('        return result')
        
        code.append('')
    
    # Add special handling for callbacks
    code.append('    # Callback management')
    code.append('    _callbacks = {}')
    code.append('')
    
    # Add specific callback handlers
    for func in functions:
        if func['name'].startswith('uwSet') and len(func['params']) > 0:
            callback_param = func['params'][0]
            if 'Callback' in callback_param['type']:
                callback_name = callback_param['type']
                func_name = func['name']
                
                # Extract callback name (remove 'uwSet' prefix and 'Callback' suffix)
                snake_case_name = func_name[5:].replace('Callback', '').lower()
                
                # Find the callback delegate definition
                delegate_pattern = r'public\s+delegate\s+(\w+)\s+' + re.escape(callback_name) + r'\s*\((.*?)\);'
                delegate_match = re.search(delegate_pattern, cs_code, re.DOTALL)
                
                if delegate_match:
                    params_str = delegate_match.group(2).strip()
                    callback_params = []
                    
                    # Parse parameters for docstring
                    if params_str:
                        for param in params_str.split(','):
                            param = param.strip()
                            if not param:
                                continue
                            
                            param_parts = param.split()
                            if len(param_parts) >= 2:
                                param_type = param_parts[0]
                                param_name = param_parts[-1]
                                callback_params.append(f"{param_name}")
                    
                    # Generate wrapper method
                    code.append(f'    @classmethod')
                    code.append(f'    def add_{snake_case_name}_callback(cls, callback_func):')
                    code.append(f'        """Add a callback for {snake_case_name} events."""')
                    code.append(f'        key = "{snake_case_name}"')
                    code.append(f'        if key not in cls._callbacks:')
                    code.append(f'            cls._callbacks[key] = []')
                    code.append(f'            cls._callbacks[key+"_func"] = cls._create_{snake_case_name}_callback()')
                    code.append(f'        cls._callbacks[key].append(callback_func)')
                    code.append(f'        return callback_func')
                    code.append('')
                    
                    # Generate internal callback creator method
                    code.append(f'    @classmethod')
                    code.append(f'    def _create_{snake_case_name}_callback(cls):')
                    code.append(f'        """Create a C callback for {snake_case_name} events."""')
                    
                    # Define callback wrapper function
                    code.append(f'        @cls.ffi.callback("{callback_name}")')
                    code.append(f'        def _callback({", ".join(callback_params)}):')
                    
                    # Process parameters for the Python callback
                    python_params = []
                    for param in params_str.split(','):
                        param = param.strip()
                        if not param:
                            continue
                        
                        param_parts = param.split()
                        if len(param_parts) >= 2:
                            param_type = param_parts[0]
                            param_name = param_parts[-1]
                            
                            # Convert C types to Python
                            if 'ref' in param:
                                struct_name = param_type.replace('ref ', '')
                                python_params.append(f"{struct_name}.from_c(cls.ffi, {param_name})")
                            elif 'string' in param_type:
                                python_params.append(f"_to_str(cls.ffi, {param_name})")
                            elif any(enum['name'] in param for enum in enums):
                                for enum in enums:
                                    if enum['name'] in param:
                                        python_params.append(f"{enum['name']}({param_name})")
                                        break
                                else:
                                    python_params.append(param_name)
                            else:
                                python_params.append(param_name)
                    
                    # Call all registered callbacks
                    code.append(f'            for cb in cls._callbacks.get("{snake_case_name}", []):')
                    code.append(f'                try:')
                    code.append(f'                    cb({", ".join(python_params)})')
                    code.append(f'                except Exception as e:')
                    code.append(f'                    print(f"Error in {snake_case_name} callback: {{e}}")')
                    code.append('')
                    
                    # Set up the callback
                    code.append(f'        # Set the callback in the API')
                    code.append(f'        cls.lib.{func_name}(_callback)')
                    code.append(f'        return _callback')
                    code.append('')
    
    # Initialize the API
    code.append('# Initialize the API on module import')
    code.append('UwApi.initialize()')
    code.append('')
    
    # For backwards compatibility, export enums at module level
    for enum in enums:
        code.append(f'# Export {enum["name"]} enum at module level for backwards compatibility')
        code.append(f'{enum["name"]} = {enum["name"]}')
    code.append('')
    
    return "\n".join(code)

if __name__ == "__main__":
    main()