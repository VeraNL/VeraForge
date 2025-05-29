# VeraForge
Compiler for the family of Vera languages (VeraPoetry, VeraDSL, VeraNL) targeting an array of executable formats (fast-agent, MCP, Ollama, dex-lang, IR, etc.)

Note: this project is in early design phases.

## Sample CLI Command

```bash
# Compile to fast-agent Python
veraforge compile examples/sensor-fusion-bot.vera --target=fast-agent --output sensor_fusion_bot.py

# Compile to IR for debugging or system visualization
veraforge compile examples/sensor-fusion-bot.vera --target=ir --output sensor_fusion_bot.vf.json
```

## VeraForgeIR Format (Example)

```json
{
  "name": "SensorFusionBot",
  "essence": ["Integrative", "Reactive", "Real-Time"],
  "purpose": "To fuse multi-modal sensor inputs into a coherent awareness frame for downstream tasks.",
  "channels": {
    "DepthSensor": {"type": "Sensor", "source": "LIDAR-X5"},
    "VisualSensor": {"type": "Sensor", "source": "VisionCam-A2"},
    "AudioSensor": {"type": "Sensor", "source": "MicArray-V1"},
    "AnalysisEngine": {"type": "Processor", "source": "EdgePredictor"}
  },
  "memory": ["RecentFrames", "ObjectPatterns", "NoiseThresholds"],
  "rituals": [
    {
      "name": "FuseInputs",
      "input": ["DepthSensor.Grid", "VisualSensor.Frame", "AudioSensor.Signals"],
      "output": "AnalysisEngine.Frame",
      "process": [
        "Synchronize(Timestamps)",
        "Normalize(DepthSensor, VisualSensor, AudioSensor)",
        "DetectObjects(VisualSensor)",
        "Fuse(DepthSensor, AudioSensor)",
        "OutputTo(AnalysisEngine)"
      ]
    }
  ]
}
```