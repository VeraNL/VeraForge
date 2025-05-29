import unittest
from veraforge.core.parser import parser
from veraforge.core.ir_builder import VeraIRBuilder
from veraforge.models.ir import VeraForgeIR

# Sample .vera archetype
sample_vera = '''
Archetype "TestBot" {
  Essence: [Simple, Modular]
  Purpose: "A test agent for parser validation."

  Channels:
    - Sensor("TestSensor") as TestInput
    - Processor("TestEngine") as TestProcessor

  Memory(["Session", "Log"]) as TestMemory

  Emanations:
    - Ritual "TestRitual" {
        Input: TestInput.Signal
        Output: TestProcessor.Output
        Process:
          -> Echo(TestInput)
          -> OutputTo(TestProcessor)
      }
}
'''

class TestVeraParser(unittest.TestCase):

    def test_parser_outputs_valid_ir(self):
        tree = parser.parse(sample_vera)
        ir = VeraIRBuilder().transform(tree)

        self.assertIsInstance(ir, VeraForgeIR)
        self.assertEqual(ir.name, "TestBot")
        self.assertEqual(len(ir.channels), 2)
        self.assertEqual(ir.memory, ["Session", "Log"])
        self.assertEqual(len(ir.rituals), 1)

        ritual = ir.rituals[0]
        self.assertEqual(ritual.name, "TestRitual")
        self.assertEqual(ritual.inputs, ["TestInput.Signal"])
        self.assertEqual(ritual.output, "TestProcessor.Output")
        self.assertIn("Echo(TestInput)", ritual.process)

if __name__ == '__main__':
    unittest.main()