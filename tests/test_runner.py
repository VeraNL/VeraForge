import json
from pathlib import Path
from veraforge.core.parser import parser
from veraforge.core.ir_builder import VeraIRBuilder
from dataclasses import asdict

VALID_DIR = Path(__file__).parent / "test_samples" / "valid"
INVALID_DIR = Path(__file__).parent / "test_samples" / "invalid"

def run_all_tests(mode="all"):
    print(f"🧪 Running VeraForge tests [mode={mode}]")

    if mode in ("all", "parse"):
        _test_valid_parsing()
        _test_invalid_parsing()

    if mode in ("all", "snapshot"):
        _test_snapshot_matches()

def _test_valid_parsing():
    print("✔️ Testing valid .vera files...")
    for vf in VALID_DIR.glob("*.vera"):
        try:
            parser.parse(vf.read_text())
            print(f"  ✓ Parsed: {vf.name}")
        except Exception as e:
            print(f"  ✗ FAILED parsing: {vf.name} — {e}")

def _test_invalid_parsing():
    print("⚠️ Testing invalid .vera files (should fail)...")
    for vf in INVALID_DIR.glob("*.vera"):
        try:
            parser.parse(vf.read_text())
            print(f"  ✗ Unexpected success: {vf.name}")
        except:
            print(f"  ✓ Correctly rejected: {vf.name}")

def _test_snapshot_matches():
    print("🔍 Testing IR snapshots...")
    for vf in VALID_DIR.glob("*.vera"):
        snapshot = vf.with_suffix(".vf.json")
        try:
            tree = parser.parse(vf.read_text())
            ir = VeraIRBuilder().transform(tree)
            actual = asdict(ir)
            expected = json.loads(snapshot.read_text())
            assert actual == expected
            print(f"  ✓ Snapshot matched: {vf.name}")
        except Exception as e:
            print(f"  ✗ Snapshot mismatch: {vf.name} — {e}")