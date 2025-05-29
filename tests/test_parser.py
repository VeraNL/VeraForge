import unittest
from pathlib import Path
from veraforge.core.parser import parser
from veraforge.core.ir_builder import VeraIRBuilder
from veraforge.models.ir import VeraForgeIR
from dataclasses import asdict

SAMPLES_PATH = Path(__file__).parent / "test_samples"

class TestFileBasedParsing(unittest.TestCase):

    def test_valid_vera_files(self):
        valid_dir = SAMPLES_PATH / "valid"
        for file in valid_dir.glob("*.vera"):
            with self.subTest(file=file):
                text = file.read_text()
                tree = parser.parse(text)
                ir = VeraIRBuilder().transform(tree)
                self.assertIsInstance(ir, VeraForgeIR)

    def test_invalid_vera_files_fail(self):
        invalid_dir = SAMPLES_PATH / "invalid"
        for file in invalid_dir.glob("*.vera"):
            with self.subTest(file=file):
                text = file.read_text()
                with self.assertRaises(Exception):
                    tree = parser.parse(text)
                    VeraIRBuilder().transform(tree)

class TestParserSnapshots(unittest.TestCase):

    def test_ir_snapshots_match(self):
        for vera_file in SAMPLES_PATH.glob("*.vera"):
            snapshot_file = vera_file.with_suffix(".vf.json")
            with self.subTest(file=vera_file.name):
                source = vera_file.read_text()
                tree = parser.parse(source)
                ir = VeraIRBuilder().transform(tree)
                current_ir_dict = asdict(ir)

                # Load expected snapshot
                expected_ir_dict = json.loads(snapshot_file.read_text())

                # Compare
                self.assertEqual(current_ir_dict, expected_ir_dict, f"Mismatch in {vera_file.name}")

if __name__ == "__main__":
    unittest.main()