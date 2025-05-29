import unittest
from pathlib import Path
from veraforge.core.parser import parser
from veraforge.core.ir_builder import VeraIRBuilder
from veraforge.models.ir import VeraForgeIR

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

if __name__ == "__main__":
    unittest.main()