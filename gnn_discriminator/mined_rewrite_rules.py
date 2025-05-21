# ✅ Auto-mined rewrite rules from high-score GNN pairs
from typing import List, Dict

def rule_000(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #1 | support count = 22"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_001(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #2 | support count = 19"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_002(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #3 | support count = 19"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_003(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #4 | support count = 18"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_004(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #5 | support count = 17"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P1",
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P1",
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_005(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #6 | support count = 17"""
    pattern = [
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_006(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #7 | support count = 16"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_007(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #8 | support count = 16"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_008(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #9 | support count = 16"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_009(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #10 | support count = 16"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_010(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #11 | support count = 15"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_011(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #12 | support count = 14"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_012(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #13 | support count = 14"""
    pattern = [
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_013(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #14 | support count = 14"""
    pattern = [
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_014(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #15 | support count = 14"""
    pattern = [
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_015(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #16 | support count = 14"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            2
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            2,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            2
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            2
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            2,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_016(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #17 | support count = 14"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_017(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #18 | support count = 14"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_018(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #19 | support count = 14"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_019(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #20 | support count = 13"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_020(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #21 | support count = 13"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_021(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #22 | support count = 13"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_022(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #23 | support count = 13"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "x",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_023(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #24 | support count = 12"""
    pattern = [
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    }
]
    replacement = [
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_024(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #25 | support count = 12"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P1",
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P3"
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P1",
            "P1"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P3"
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_025(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #26 | support count = 12"""
    pattern = [
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_026(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #27 | support count = 12"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_027(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #28 | support count = 12"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_028(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #29 | support count = 12"""
    pattern = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            1
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    }
]
    replacement = [
    {
        "name": "add",
        "qubits": [],
        "params": [
            "P0",
            "P0"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            1,
            0
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P1"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            1
        ],
        "params": [
            "P2"
        ]
    },
    {
        "name": "cx",
        "qubits": [
            0,
            1
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

def rule_029(gates: List[Dict], pos: int) -> List[Dict]:
    """Auto-mined rule #30 | support count = 11"""
    pattern = [
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    }
]
    replacement = [
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "rz",
        "qubits": [
            0
        ],
        "params": [
            "P0"
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    },
    {
        "name": "x",
        "qubits": [
            0
        ]
    },
    {
        "name": "h",
        "qubits": [
            0
        ]
    }
]
    if gates[pos:pos+len(pattern)] == pattern:
        return gates[:pos] + replacement + gates[pos+len(pattern):]
    return gates

