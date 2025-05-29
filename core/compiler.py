from .parser import vera_parser
from .ir_builder import VeraIRBuilder
from .targets.fast_agent_codegen import generate_fast_agent_code
# other target imports go here

def compile_vera(input_path: str, target: str, output_path: str):
    with open(input_path, 'r') as f:
        vera_code = f.read()

    # Step 1: Parse
    tree = parser.parse(vera_code)

    # Step 2: Transform → IR
    ir = VeraIRBuilder().transform(tree)

    # Step 3: Compile to target
    if target == "fast-agent":
        code = generate_fast_agent_code(ir)
        with open(output_path, 'w') as out:
            out.write(code)

    elif target == "ir":
        import json
        with open(output_path, 'w') as out:
            json.dump(ir.__dict__, out, indent=2)

    else:
        raise ValueError(f"Unsupported target: {target}")