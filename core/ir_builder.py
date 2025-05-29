# Builds VeraForgeIR from AST

from lark import Lark, Transformer
from dataclasses import dataclass
from typing import List

# ---------- VeraDSL Grammar ----------
vera_grammar = r"""
    start: archetype

    archetype: "Archetype" ESCAPED_STRING "{" body "}"
    body: (essence | purpose | channels | memory | emanations)+

    essence: "Essence:" "[" [IDENT ("," IDENT)*] "]"
    purpose: "Purpose:" ESCAPED_STRING

    channels: "Channels:" channel_list
    channel_list: "-" channel (NEWLINE "-" channel)*
    channel: sensor | processor
    sensor: "Sensor(" ESCAPED_STRING ")" "as" IDENT
    processor: "Processor(" ESCAPED_STRING ")" "as" IDENT

    memory: "Memory(" "[" [ESCAPED_STRING ("," ESCAPED_STRING)*] "]" ")" "as" IDENT

    emanations: "Emanations:" "-" ritual
    ritual: "Ritual" ESCAPED_STRING "{" ritual_body "}"
    ritual_body: "Input:" input_list NEWLINE
                 "Output:" IDENT "." IDENT NEWLINE
                 "Process:" process_list

    input_list: IDENT "." IDENT ("," IDENT "." IDENT)*
    process_list: "->" process_step (NEWLINE "->" process_step)*
    process_step: /[a-zA-Z_]+(\([^\)]*\))?/

    IDENT: /[A-Za-z_][A-Za-z0-9_]*/
    NEWLINE: /(\r?\n)+/

    %import common.ESCAPED_STRING
    %import common.WS_INLINE
    %ignore WS_INLINE
    %ignore NEWLINE
"""

# ---------- IR Data Classes ----------
@dataclass
class Channel:
    kind: str
    source: str
    alias: str

@dataclass
class Ritual:
    name: str
    inputs: List[str]
    output: str
    process: List[str]

@dataclass
class VeraForgeIR:
    name: str
    essence: List[str]
    purpose: str
    channels: List[Channel]
    memory: List[str]
    rituals: List[Ritual]

# ---------- AST to IR Transformer ----------
class VeraIRBuilder(Transformer):
    def ESCAPED_STRING(self, s):
        return s[1:-1]

    def IDENT(self, s):
        return str(s)

    def archetype(self, items):
        name = items[0]
        props = {k: v for d in items[1:] for k, v in d.items()}
        return VeraForgeIR(
            name=name,
            essence=props.get("essence", []),
            purpose=props.get("purpose", ""),
            channels=props.get("channels", []),
            memory=props.get("memory", []),
            rituals=props.get("rituals", [])
        )

    def essence(self, items):
        return {"essence": items}

    def purpose(self, items):
        return {"purpose": items[0]}

    def sensor(self, items):
        return Channel(kind="Sensor", source=items[0], alias=items[1])

    def processor(self, items):
        return Channel(kind="Processor", source=items[0], alias=items[1])

    def channel_list(self, items):
        return {"channels": items}

    def memory(self, items):
        return {"memory": items[0]}

    def ritual(self, items):
        name = items[0]
        body = items[1]
        return {"rituals": [Ritual(name=name, **body)]}

    def ritual_body(self, items):
        return {
            "inputs": items[0],
            "output": f"{items[1]}.{items[2]}",
            "process": items[3]
        }

    def input_list(self, items):
        return [f"{items[i]}.{items[i+1]}" for i in range(0, len(items), 2)]

    def process_list(self, items):
        return items

    def process_step(self, s):
        return str(s)

# ---------- Sample VeraDSL Input ----------
vera_code = '''
Archetype "SensorFusionBot" {
  Essence: [Integrative, Reactive, Real-Time]
  Purpose: "To fuse multi-modal sensor inputs into a coherent awareness frame for downstream tasks."

  Channels:
    - Sensor("LIDAR-X5") as DepthSensor
    - Sensor("VisionCam-A2") as VisualSensor
    - Sensor("MicArray-V1") as AudioSensor
    - Processor("EdgePredictor") as AnalysisEngine

  Memory(["RecentFrames", "ObjectPatterns", "NoiseThresholds"]) as FusionMemory

  Emanations:
    - Ritual "FuseInputs" {
        Input: DepthSensor.Grid, VisualSensor.Frame, AudioSensor.Signals
        Output: AnalysisEngine.Frame
        Process:
          -> Synchronize(Timestamps)
          -> Normalize(DepthSensor, VisualSensor, AudioSensor)
          -> DetectObjects(VisualSensor)
          -> Fuse(DepthSensor, AudioSensor)
          -> OutputTo(AnalysisEngine)
      }
}
'''

# ---------- Run Parser ----------
parser = Lark(vera_grammar, parser='lalr', start='start')
tree = parser.parse(vera_code)
ir = VeraIRBuilder().transform(tree)

print(ir)