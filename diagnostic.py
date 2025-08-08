import sys
import quartz

print("--- Quartz API Diagnostics ---")
print(f"Python version: {sys.version.split()[0]}")
print(f"Quartz module loaded from: {quartz.__file__}")

gate_name_str = 'h'
gate_type_from_func = None

print("\n[1] Testing quartz.get_gate_type_from_str()...")
try:
    gate_type_from_func = quartz.get_gate_type_from_str(gate_name_str)
    print(f"    SUCCESS: quartz.get_gate_type_from_str('{gate_name_str}') executed.")
    print(f"    Return value: {gate_type_from_func}")
    print(f"    Type of return value: {type(gate_type_from_func)}")
except Exception as e:
    print(f"    FAILED: {e}")

print("\n[2] Trying to find the GateType enum itself...")
FoundGateType = None
try:
    # 尝试直接访问 quartz.GateType
    FoundGateType = quartz.GateType
    print("    SUCCESS: Found quartz.GateType.")
except AttributeError:
    # 如果直接访问失败，尝试访问 quartz.core.GateType
    print("    INFO: quartz.GateType not found. Trying quartz.core.GateType...")
    try:
        FoundGateType = quartz.core.GateType
        print("    SUCCESS: Found quartz.core.GateType.")
    except AttributeError:
        print("    FAILED: Could not find GateType in quartz or quartz.core.")
    except Exception as e:
        print(f"    FAILED with other error when accessing quartz.core.GateType: {e}")
except Exception as e:
    print(f"    FAILED with other error when accessing quartz.GateType: {e}")

if FoundGateType:
    print("\n[3] Analyzing the found GateType enum...")
    try:
        h_gate_enum = FoundGateType.h
        print(f"    Type of GateType.h enum member: {type(h_gate_enum)}")
        print(f"    Value of GateType.h enum member: {h_gate_enum.value}")
        print(f"    Is GateType.h == result from get_gate_type_from_str? {h_gate_enum == gate_type_from_func}")
        print(f"    Is GateType.h.value == result from get_gate_type_from_str? {h_gate_enum.value == gate_type_from_func}")
    except Exception as e:
        print(f"    FAILED to analyze GateType members: {e}")

print("\n--- Diagnostics Complete ---")
