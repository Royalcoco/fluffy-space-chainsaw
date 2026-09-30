#!/usr/bin/env python3
"""
cone_tape.py
Binary tape state machine for cone.txt save/load workflow
Guessed interpretation of: tape binairie 101 011 :/011, 011:/101 110/:/EXIT
"""

class ConeTape:
    def __init__(self):
        self.states = {
            5:   {"desktop": "home", "task": "clarify"},    # 101
            3:   {"desktop": "plan", "task": "plan"},        # 011
            6:   {"desktop": "setup", "task": "setup"},      # 110
        }
        self.tape = [
            ("101", "011", ":/011"),  # state 5 -> 3, save to 011
            ("011", "101", "110:/"),  # state 3 -> 5, load from 110
            ("EXIT",)
        ]
        self.current_state = 5
        self.saved_states = {}
    
    def execute_tape(self):
        """Execute the binary tape sequence"""
        print("=== CONE TAPE EXECUTOR ===\n")
        
        for instruction in self.tape:
            if instruction[0] == "EXIT":
                print("✓ TAPE COMPLETE")
                break
            
            from_state, to_state, operation = instruction
            from_state_dec = int(from_state, 2)
            to_state_dec = int(to_state, 2)
            
            if from_state_dec == self.current_state:
                print(f"→ Transition: {from_state} ({from_state_dec}) → {to_state} ({to_state_dec})")
                print(f"  State data: {self.states.get(from_state_dec, 'unknown')}")
                
                if ":" in operation:
                    parts = operation.split(":")
                    if parts[0] == "":
                        # :/target format (save)
                        target = parts[1]
                        self.save_state(from_state_dec, target)
                    elif parts[1] == "":
                        # source:/ format (load)
                        source = parts[0]
                        self.load_state(to_state_dec, source)
                
                self.current_state = to_state_dec
                print()
    
    def save_state(self, state_num, target):
        """Save current state to tape position"""
        state_data = self.states.get(state_num, {})
        self.saved_states[target] = state_data
        print(f"  💾 SAVE: state {state_num} → tape[{target}]")
        print(f"     Data: {state_data}")
    
    def load_state(self, state_num, source):
        """Load state from tape position"""
        loaded_data = self.saved_states.get(source, {})
        print(f"  📂 LOAD: tape[{source}] → state {state_num}")
        print(f"     Data: {loaded_data}")
    
    def get_state(self, state_num):
        """Get state by number"""
        return self.states.get(state_num, None)
    
    def print_states(self):
        """Print all available states"""
        print("\n=== STATE REGISTRY ===")
        for num, data in self.states.items():
            print(f"State {num} (binary: {bin(num)[2:].zfill(3)}): {data}")


if __name__ == "__main__":
    tape = ConeTape()
    tape.print_states()
    print()
    tape.execute_tape()
    
    print("=== SAVED CHECKPOINTS ===")
    for checkpoint, data in tape.saved_states.items():
        print(f"Checkpoint {checkpoint}: {data}")
