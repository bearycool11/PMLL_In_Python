import socket
import struct

# Define the structure for a node in the graph
class Node:
    def __init__(self, entity, hash_val):
        self.entity = entity
        self.hash = hash_val
        self.next = None  # Linked list for possible expansion

# Define the structure for an edge in the graph
class Edge:
    def __init__(self, from_node, to_node, relationship, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.relationship = relationship
        self.weight = weight

# Define the structure for the graph
class Graph:
    def __init__(self, initial_capacity):
        self.nodes = []
        self.edges = []
        self.capacity_nodes = initial_capacity
        self.capacity_edges = initial_capacity

    def add_node(self, node):
        if len(self.nodes) >= self.capacity_nodes:
            self.capacity_nodes *= 2
        self.nodes.append(node)

    def add_edge(self, edge):
        if len(self.edges) >= self.capacity_edges:
            self.capacity_edges *= 2
        self.edges.append(edge)

# Define the memory association system
class MemoryAssoc:
    def __init__(self, seed):
        self.graph = Graph(10)  # Initialize the graph with an initial capacity
        self.seed = seed

    def create_node(self, entity, hash_val):
        return Node(entity, hash_val)

    def create_edge(self, from_node, to_node, relationship, weight):
        return Edge(from_node, to_node, relationship, weight)

    def add_entity(self, entity, hash_val):
        new_node = self.create_node(entity, hash_val)
        self.graph.add_node(new_node)

    def add_relationship(self, entity1, entity2, relationship, weight):
        node1 = None
        node2 = None

        # Find or create nodes
        for node in self.graph.nodes:
            if node.entity == entity1:
                node1 = node
            if node.entity == entity2:
                node2 = node

        if not node1:
            node1 = self.create_node(entity1, 0)
            self.graph.add_node(node1)
        if not node2:
            node2 = self.create_node(entity2, 0)
            self.graph.add_node(node2)

        edge = self.create_edge(node1, node2, relationship, weight)
        self.graph.add_edge(edge)

        # Log the relationship addition
        print(f"Added relationship: {entity1} -> {entity2} ({relationship}, {weight})")

    def get_relationships_memory_assoc(self, entity):
        print(f"Fetching relationships for: {entity}")
        for edge in self.graph.edges:
            if edge.from_node.entity == entity:
                print(f"Relationship: {edge.from_node.entity} -> {edge.to_node.entity} ({edge.relationship}, {edge.weight})")

    def fetch_relationships_from_socket(self, entity):
        server_ip = "127.0.0.1"
        server_port = 8080
        try:
            socket_fd = self.create_io_socket(server_ip, server_port)
            if socket_fd < 0:
                print("Failed to connect to the relationship server.")
                return

            # Send request to fetch relationships
            request = f"GET_RELATIONSHIPS {entity}\n"
            self.io_socket_write(socket_fd, request.encode())

            # Receive response from the server
            response = self.io_socket_read(socket_fd)
            print(f"Server Response: {response}")

            # Parse response and update the graph
            lines = response.split("\n")
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) == 4:
                        entity1, entity2, relationship, weight = parts
                        weight = int(weight)
                        self.add_relationship(entity1, entity2, relationship, weight)

            # Cleanup
            self.io_socket_cleanup(socket_fd)
        except Exception as e:
            print(f"Error fetching relationships: {e}")

    def create_io_socket(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            return sock
        except socket.error as e:
            print(f"Socket creation or connection failed: {e}")
            return -1

    def io_socket_write(self, sock, data):
        try:
            sock.sendall(data)
        except socket.error as e:
            print(f"Socket write failed: {e}")

    def io_socket_read(self, sock):
        try:
            buffer = sock.recv(1024)
            return buffer.decode()
        except socket.error as e:
            print(f"Socket read failed: {e}")
            return ""

    def io_socket_cleanup(self, sock):
        sock.close()


# Example usage
if __name__ == "__main__":
    memory_assoc = MemoryAssoc(seed=42)

    # Add entities and relationships
    memory_assoc.add_entity("Entity1", 1)
    memory_assoc.add_entity("Entity2", 2)
    memory_assoc.add_relationship("Entity1", "Entity2", "Relationship", 3)

    # Fetch additional relationships dynamically from a socket
    memory_assoc.fetch_relationships_from_socket("Entity1")

    # Display relationships
    memory_assoc.get_relationships_memory_assoc("Entity1")
