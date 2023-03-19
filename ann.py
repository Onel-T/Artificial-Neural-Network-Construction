class node:
    def __init__(self, connections):
        self.connections = connections
        self.collector = 0.0


# Returns list of numbers from csv
def strip_csv(csv):
    list_of_nums = []

    with open(csv, "r") as csv_file:
        nums_string = csv_file.read().split(',')
    
    # Convert each number to an int or float
    for n in nums_string:
        try:
            list_of_nums.append(int(n)) 
        except:
            list_of_nums.append(float(n))

    return list_of_nums


def create_layer(number_of_nodes):
    new_layer = []
    # Loop amount of nodes
    for i in range(number_of_nodes):
        new_layer.append(node(None)) # Appending node object with no connections
    
    return new_layer


def create_connections(network):
    # Connecting layer n to layer n+1 (last layer is connected to none)
    for layer in range(len(network) - 1):
        for node_in_layer in range(len(network[layer])):
            network[layer][node_in_layer].connections = network[layer + 1]


def create_network(nodes_per_layer):
    network = []

    # Loop amount of layers to create each layer
    for num_nodes in nodes_per_layer:
        network.append(create_layer(num_nodes))

    create_connections(network)

    return network


def propagate_input(network, input_numbers):
    # Storing input values in first layer
    for i in range(len(network[0])):
        network[0][i].collector = input_numbers[i]

    # Loop for number of layers (excluding the last layer)
    for layer in range(len(network) - 1):
        # Loop for number of nodes in the current layer
        for node in network[layer]:
            # Loop for number of connections in the current node
            for connected_node in node.connections:
                # Accessing the collector for each connection to the node
                connected_node.collector = connected_node.collector + node.collector
    

if __name__ == '__main__':
    nodes_per_layer = strip_csv("network.txt")
    input_nums = strip_csv("input.txt")

    network = create_network(nodes_per_layer)

    propagate_input(network, input_nums)

    # Print out the value of each node in the last layer
    for n in range(len(network[-1])):
        print(network[-1][n].collector)

