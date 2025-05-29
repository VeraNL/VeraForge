# Codegen logic for fast-agent Python

def generate_fast_agent_code(ir: VeraForgeIR) -> str:
    lines = []

    lines.append("from fast_agent.agent import Agent")
    lines.append("from fast_agent.nodes import SensorNode, ProcessorNode, MemoryNode")
    lines.append("from fast_agent.utils import synchronize, normalize, detect_objects, fuse\n")

    lines.append(f"class {ir.name}(Agent):")
    lines.append("    def __init__(self):")
    lines.append(f'        super().__init__(')
    lines.append(f'            name="{ir.name}",')
    lines.append(f'            essence={ir.essence},')
    lines.append(f'            purpose="{ir.purpose}"')
    lines.append('        )\n')

    # Channels
    lines.append("        # Channels")
    for ch in ir.channels:
        node_type = "SensorNode" if ch.kind == "Sensor" else "ProcessorNode"
        lines.append(f'        self.{ch.alias} = {node_type}("{ch.source}")')
    lines.append("")

    # Memory
    if ir.memory:
        mem_keys = ', '.join([f'"{m}"' for m in ir.memory])
        lines.append(f'        self.FusionMemory = MemoryNode([{mem_keys}])\n')

    # Ritual bindings
    lines.append("        # Rituals")
    for ritual in ir.rituals:
        lines.append(f'        self.add_ritual("{ritual.name}", self.{ritual.name})')
    lines.append("")

    # Ritual methods
    for ritual in ir.rituals:
        lines.append(f"    def {ritual.name}(self, inputs):")

        # Inputs
        for input_expr in ritual.inputs:
            chan, attr = input_expr.split(".")
            lines.append(f'        {chan}_{attr} = self.{chan}.read("{attr}")')

        # Placeholder for processing steps
        lines.append("")
        lines.append("        # Processing steps")
        for step in ritual.process:
            lines.append(f"        {step}  # TODO: Implement")

        # Output
        output_chan, output_attr = ritual.output.split(".")
        lines.append(f'\n        self.{output_chan}.send("{output_attr}", result)  # Final output placeholder\n')

    return "\n".join(lines)