# Master CLI wrapper

#!/usr/bin/env python3
import argparse
import sys
from veraforge.core.compiler import compile_vera
from tests.test_runner import run_all_tests

def main():
    parser = argparse.ArgumentParser(
        description="🛠️ VeraForge CLI — Compiler & Test Suite for the VeraDSL archetypal language."
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # --- compile command ---
    compile_parser = subparsers.add_parser("compile", help="Compile a .vera file to target code or IR")
    compile_parser.add_argument("input", help="Path to .vera file")
    compile_parser.add_argument("--target", choices=["fast-agent", "ir"], required=True, help="Target format")
    compile_parser.add_argument("--output", required=True, help="Path to output file")

    # --- test command ---
    test_parser = subparsers.add_parser("test", help="Run VeraForge parser and snapshot tests")
    test_parser.add_argument("--mode", choices=["all", "snapshot", "parse"], default="all")

    args = parser.parse_args()

    if args.command == "compile":
        compile_vera(args.input, args.target, args.output)
    elif args.command == "test":
        run_all_tests(mode=args.mode)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()