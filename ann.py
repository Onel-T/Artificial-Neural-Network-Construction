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


def create_layer(number_of_nodes, last_layer):
    new_layer = []
    # Loop amount of nodes
    for i in range(number_of_nodes):
        new_layer.append(node(last_layer))
    
    return new_layer


def create_connections(network):
    # Connecting layer n to layer n+1 (last layer is connected to none)
    for layer in range(len(network) - 1):
        for node_in_layer in range(len(network[layer])):
            network[layer][node_in_layer].connections = network[layer + 1]


def create_network(nodes_per_layer):
    last_layer = None
    network = []

    # Loop amount of elements (layers)
    for num_nodes in nodes_per_layer:
        network.append(create_layer(num_nodes, last_layer))

    create_connections(network)

    return network

    

if __name__ == '__main__':
    nodes_per_layer = strip_csv("network.txt")
    input_nums = strip_csv("input.txt")

    network = create_network(nodes_per_layer)




