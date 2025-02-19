import threading
import os

class PMLL:
    def __init__(self, file_name):
        self.memory_file = file_name
        self.memory = {}  # Key-value memory store
        self.memory_lock = threading.Lock()  # Thread safety
        self.load_memory()  # Load memory from file upon initialization

    def __del__(self):
        self.save_memory()  # Save memory to file when the object is destroyed

    def load_memory(self):
        with self.memory_lock:  # Ensure thread safety
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, 'r') as infile:
                        while True:
                            key = infile.readline().strip()
                            if not key:
                                break
                            value = infile.readline().strip()
                            self.memory[key] = value
                except IOError:
                    print("Error: Could not open memory file for reading.")
            else:
                print("Memory file does not exist. Starting with an empty memory.")

    def save_memory(self):
        with self.memory_lock:  # Ensure thread safety
            try:
                with open(self.memory_file, 'w') as outfile:
                    for key, value in self.memory.items():
                        outfile.write(f"{key}\n{value}\n")  # Write each key-value pair
            except IOError:
                print("Error: Could not open memory file for writing.")

    def add_memory(self, key, value):
        with self.memory_lock:  # Ensure thread safety
            self.memory[key] = value  # Add or update the key-value pair

    def get_memory(self, key):
        with self.memory_lock:  # Ensure thread safety
            return self.memory.get(key, "")  # Return value or empty string if key doesn't exist

    def clear_memory(self):
        with self.memory_lock:  # Ensure thread safety
            self.memory.clear()  # Clear all memory entries

    def display_memory(self):
        with self.memory_lock:  # Ensure thread safety
            if not self.memory:
                print("Memory is empty.")
            else:
                for key, value in self.memory.items():
                    print(f"Key: {key} | Value: {value}")


# Example usage:
if __name__ == "__main__":
    pmll = PMLL("memory.txt")  # Initialize with the file name

    # Add or update memory entries
    pmll.add_memory("name", "John Doe")
    pmll.add_memory("age", "30")

    # Retrieve memory entries
    print(pmll.get_memory("name"))  # Outputs: John Doe
    print(pmll.get_memory("age"))  # Outputs: 30

    # Display all memory entries
    pmll.display_memory()

    # Clear memory entries
    pmll.clear_memory()
    pmll.display_memory()  # Should print "Memory is empty."

    # Saving memory to file happens automatically when the object is destroyed.
