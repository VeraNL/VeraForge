import json
from pathlib import Path
from veraforge.core.parser import parser
from veraforge.core.ir_builder import VeraIRBuilder
from dataclasses import asdict

# Path to valid test samples
VALID_PATH = Path(__file__).parent.parent / "tests" / "test_samples" / "valid"

def generate_snapshot(vera_file: Path):
    try:
        print(f"Generating snapshot for {vera_file.name}")
        vera_code = vera_file.read_text()
        tree = parser.parse(vera_code)
        ir = VeraIRBuilder().transform(tree)
        snapshot_data = asdict(ir)

        snapshot_file = vera_file.with_suffix(".vf.json")
        snapshot_file.write_text(json.dumps(snapshot_data, indent=2))
        print(f"✓ Saved snapshot: {snapshot_file.name}")
    except Exception as e:
        print(f"✗ Failed to generate snapshot for {vera_file.name}: {e}")

def generate_all_snapshots():
    print("🌟 Generating all valid snapshots...")
    for vera_file in VALID_PATH.glob("*.vera"):
        generate_snapshot(vera_file)

if __name__ == "__main__":
    generate_all_snapshots()