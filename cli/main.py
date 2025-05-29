# CLI entrypoint (e.g. `veraforge compile`)

import argparse
from core.compiler import compile_vera

def main():
    parser = argparse.ArgumentParser(description="VeraForge CLI")
    parser.add_argument("command", choices=["compile"])
    parser.add_argument("input", help="Path to .vera file")
    parser.add_argument("--target", choices=["fast-agent", "ir"], required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "compile":
        compile_vera(input_path=args.input, target=args.target, output_path=args.output)

if name == "main":
    main()