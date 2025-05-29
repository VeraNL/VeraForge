from core.targets.fast_agent import generate_fast_agent_code

code = generate_fast_agent_code(ir)

with open("sensor_fusion_bot.py", "w") as f:
    f.write(code)