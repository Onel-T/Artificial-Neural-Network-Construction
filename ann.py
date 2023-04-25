import random
import math

class node:
    def __init__(self, connections):
        self.connections = connections
        self.collector = 0.0
        self.weights = []
        self.delta = 0.0

# Returns list of numbers from network structure csv
def strip_network_csv(csv):
    list_of_nums = []

    with open(csv, "r") as csv_file:
        nums_string = csv_file.read().split(',')
    
    # Convert each number to an int or float
    for n in nums_string:
        list_of_nums.append(int(n)) 
    
    return list_of_nums

# Returns 2d list of numbers from the input csv
def strip_input_csv(csv):
    list_of_nums = []

    with open(csv, "r") as csv_file:
        nums_string = csv_file.read().split('\n')
    
    # Convert each number to an int or float
    for n in nums_string:
        try:
            temp = [int(num) for num in n.split(',')]
        except:
            temp = [float(num) for num in n.split(',')]
        
        list_of_nums.append(temp) 
    
    return list_of_nums


def create_layer(number_of_nodes):
    new_layer = []
    # Loop amount of nodes
    for i in range(number_of_nodes):
        new_layer.append(node(None)) # Appending node object with no connections
    
    return new_layer

# Creates connections and weights
def create_connections(network):
    # Connecting layer n to layer n+1 (last layer is connected to none)
    for layer in range(len(network) - 1):
        for node_in_layer in range(len(network[layer])):
            network[layer][node_in_layer].connections = network[layer + 1]

def create_weights(network):
    # Skip first layer then add weights to next layers
    for layer in range(1, len(network), 1):
        for node_in_layer in range(len(network[layer])):
            for previous_layer_nodes in range(len(network[layer-1])):
                network[layer][node_in_layer].weights.append(random.random())

def create_network(nodes_per_layer):
    network = []

    # Loop amount of layers to create each layer
    for num_nodes in nodes_per_layer:
        network.append(create_layer(num_nodes))

    create_connections(network)
    create_weights(network)

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

class network:
    def __init__(self, network):
        self.network = network

    # Node activation
    def activate(self, node, inputs):
        activation = 0
        for i in range(len(node.weights)):
            # Node will have all the weights from connection to previous layer
            activation += node.weights[i] * inputs[i]   # sum(weight_i * input_i)

        node.collector = self.transfer(activation)

        return node.collector

    def transfer(self, activation):
        return 1.0 / (1.0 + math.exp(-activation))

    # Sigmoid transfer function 
    def transfer_derivative(self, node):
        return node.collector * (1.0 - node.collector)

    def forward_propagate(self, input_row):
        input = input_row

        # First layer gets input
        for i in range(len(self.network[0])): 
            self.network[0][i].collector = input[i]

        # Feed Forward
        for layer in range(1, len(self.network), 1): # Skip input layer (layer 0)
            next_input = []
            for node in self.network[layer]:
                self.activate(node, input)
                next_input.append(node.collector)
            input = next_input
            
        return input  

    def backward_propagate_error(self, expected):
        # Iterating through layers in reversed order 
        for i in reversed(range(len(self.network))): 
            layer = self.network[i]
            errors = []

            if i != len(self.network) - 1:  # if not on output layer (last layer)
                # Calculate error for current layer
                for j in range(len(layer)):
                    error = 0.0
                    for node in self.network[i + 1]:    # using nodes in front of current layer for the weights
                        error += (node.weights[j] * node.delta) 
                    errors.append(error)
            else: # Currently on the output layer (last layer)
                # Calculate error for output layer
                for j in range(len(layer)):
                    node = layer[j]
                    errors.append(node.collector - expected[j])

            # Update the delta for nodes in the layer
            for j in range(len(layer)):
                node = layer[j]
                node.delta = errors[j] * self.transfer_derivative(node)

    # Using the delta from backward propagation to update weights
    def update_weights(self, l_rate):
        # Loop through the layers
        for layer in range(1, len(self.network), 1):    # Skipping input layer b/c doesn't have weights
            # Need list of collectors from previous layer as input
            inputs = [node.collector for node in self.network[layer - 1]]   

            # Updating weights
            for node in self.network[layer]:
                for i in range(len(inputs)):
                    # updating each weight connected to current node
                    node.weights[i] -= l_rate * node.delta * inputs[i]            

    def train_network(self,  train, l_rate, n_epoch, target_error):
        number_of_inputs = len(self.network[0])
        for epoch in range(n_epoch):
            sum_error = 0
            for row in train:
                self.forward_propagate(row)
                expected = []   # expected output of network
                for i in range( len(self.network[-1] )):
                    expected.append(row[number_of_inputs + i])
                    sum_error += (row[number_of_inputs + i] - self.network[-1][i].collector)**2
                if sum_error <= target_error:
                    print("Target Error Reached error=%.3f" % ( sum_error))
                    return
                self.backward_propagate_error(expected)
                self.update_weights(l_rate)
            print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))


if __name__ == '__main__':
    nodes_per_layer = strip_network_csv("network.txt")
    input_nums = strip_input_csv("input.txt")

    # 2d list containing layers and node objects in each layer  ( network[layer][node] )
    created_network = create_network(nodes_per_layer)

    network_obj = network(created_network)
    network_obj.train_network(input_nums, 0.1, 1000, 0.05)


    # print(network)
    # propagate_input(network, input_nums)

    # Print out the value of each node in the last layer
    # for n in range(len(network[-1])):
    #     print(network[-1][n].collector)

