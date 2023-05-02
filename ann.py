import random
import math
import sqlite3

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
    
    # Convert each number to an int
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

# Creates connections
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


class network:
    def __init__(self, network):
        self.network = network

    # Node activation and runs transfer
    def activate(self, node, inputs):
        activation = 0
        for i in range(len(node.weights)):
            # Node will have all the weights from connection to previous layer
            activation += node.weights[i] * inputs[i]   # sum(weight_i * input_i)
        node.collector = self.transfer(activation)

    # Sigmoid
    def transfer(self, activation):
        return 1.0 / (1.0 + math.exp(-activation))

    def transfer_derivative(self, node):
        return node.collector * (1.0 - node.collector)

    def forward_propagate(self, input_row):
        input = input_row

        # First layer gets input
        for i in range(len(self.network[0])): 
            self.network[0][i].collector = input[i]

        # Feed Forward (first loop uses the input_row passed in)
        for layer in range(1, len(self.network), 1): # Skip input layer (layer 0)
            next_input = []
            for node in self.network[layer]:
                self.activate(node, input)  # activates node.collector
                next_input.append(node.collector)
            input = next_input
            

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
            # Using collectors from previous layer as input
            inputs = [node.collector for node in self.network[layer - 1]]  

            # Updating weights
            for node in self.network[layer]:
                for i in range(len(inputs)):
                    # updating each weight connected to current node
                    node.weights[i] -= l_rate * node.delta * inputs[i]            

    def train_network(self, train, l_rate, n_epoch, target_error):
        number_of_inputs = len(self.network[0])
        for epoch in range(n_epoch):
            sum_error = 0
            for row in train:
                self.forward_propagate(row)
                expected = []   # expected output of network
                for i in range( len(self.network[-1] )):
                    expected.append(row[number_of_inputs + i])
                    sum_error += (row[number_of_inputs + i] - self.network[-1][i].collector)**2
                self.backward_propagate_error(expected)
                self.update_weights(l_rate)

            print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))    
            
            if sum_error <= target_error:
                print("Target Error Reached error=%.3f" % ( sum_error))
                return


if __name__ == '__main__':
    nodes_per_layer = strip_network_csv("network.txt")
    # input_nums = strip_input_csv("input.txt")

    # 2d list containing layers and node objects in each layer  ( network[layer][node] )
    created_network = create_network(nodes_per_layer)

    data_base = sqlite3.connect("hw_data") 
    cur = data_base.cursor()

    res = cur.execute("""select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27
    ,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,a38,a39,a40,a41,a42,a43,a44,a45,a46,a47,a48,a49,a50,a51,a52,a53,a54,a55
    ,a56,a57,a58,a59,a60,a61,a62,a63,a64,a65,a66,a67,a68,a69,a70,a71,a72,a73,a74,a75,a76,a77,a78,a79,a80,a81,a82,a83
    ,a84,a85,a86,a87,a88,a89,a90,a91,a92,a93,a94,a95,a96,a97,a98,a99,a100,a101,a102,a103,a104,a105,a106,a107,a108,a109,a110,a111
    ,a112,a113,a114,a115,a116,a117,a118,a119,a120,a121,a122,a123,a124,a125,a126,a127,a128,a129,a130,a131,a132,a133,a134,a135,a136,a137,a138,a139
    ,a140,a141,a142,a143,a144,a145,a146,a147,a148,a149,a150,a151,a152,a153,a154,a155,a156,a157,a158,a159,a160,a161,a162,a163,a164,a165,a166,a167
    ,a168,a169,a170,a171,a172,a173,a174,a175,a176,a177,a178,a179,a180,a181,a182,a183,a184,a185,a186,a187,a188,a189,a190,a191,a192,a193,a194,a195
    ,a196,a197,a198,a199,a200,a201,a202,a203,a204,a205,a206,a207,a208,a209,a210,a211,a212,a213,a214,a215,a216,a217,a218,a219,a220,a221,a222,a223
    ,a224,a225,a226,a227,a228,a229,a230,a231,a232,a233,a234,a235,a236,a237,a238,a239,a240,a241,a242,a243,a244,a245,a246,a247,a248,a249,a250,a251
    ,a252,a253,a254,a255,a256,a257,a258,a259,a260,a261,a262,a263,a264,a265,a266,a267,a268,a269,a270,a271,a272,a273,a274,a275,a276,a277,a278,a279
    ,a280,a281,a282,a283,a284,a285,a286,a287,a288,a289,a290,a291,a292,a293,a294,a295,a296,a297,a298,a299,a300,a301,a302,a303,a304,a305,a306,a307
    ,a308,a309,a310,a311,a312,a313,a314,a315,a316,a317,a318,a319,a320,a321,a322,a323,a324,a325,a326,a327,a328,a329,a330,a331,a332,a333,a334,a335
    ,a336,a337,a338,a339,a340,a341,a342,a343,a344,a345,a346,a347,a348,a349,a350,a351,a352,a353,a354,a355,a356,a357,a358,a359,a360,a361,a362,a363
    ,a364,a365,a366,a367,a368,a369,a370,a371,a372,a373,a374,a375,a376,a377,a378,a379,a380,a381,a382,a383,a384,a385,a386,a387,a388,a389,a390,a391
    ,a392,a393,a394,a395,a396,a397,a398,a399,a400,a401,a402,a403,a404,a405,a406,a407,a408,a409,a410,a411,a412,a413,a414,a415,a416,a417,a418,a419
    ,a420,a421,a422,a423,a424,a425,a426,a427,a428,a429,a430,a431,a432,a433,a434,a435,a436,a437,a438,a439,a440,a441,a442,a443,a444,a445,a446,a447
    ,a448,a449,a450,a451,a452,a453,a454,a455,a456,a457,a458,a459,a460,a461,a462,a463,a464,a465,a466,a467,a468,a469,a470,a471,a472,a473,a474,a475
    ,a476,a477,a478,a479,a480,a481,a482,a483,a484,a485,a486,a487,a488,a489,a490,a491,a492,a493,a494,a495,a496,a497,a498,a499,a500,a501,a502,a503
    ,a504,a505,a506,a507,a508,a509,a510,a511,a512,a513,a514,a515,a516,a517,a518,a519,a520,a521,a522,a523,a524,a525,a526,a527,a528,a529,a530,a531
    ,a532,a533,a534,a535,a536,a537,a538,a539,a540,a541,a542,a543,a544,a545,a546,a547,a548,a549,a550,a551,a552,a553,a554,a555,a556,a557,a558,a559
    ,a560,a561,a562,a563,a564,a565,a566,a567,a568,a569,a570,a571,a572,a573,a574,a575,a576,a577,a578,a579,a580,a581,a582,a583,a584,a585,a586,a587
    ,a588,a589,a590,a591,a592,a593,a594,a595,a596,a597,a598,a599,a600,a601,a602,a603,a604,a605,a606,a607,a608,a609,a610,a611,a612,a613,a614,a615
    ,a616,a617,a618,a619,a620,a621,a622,a623,a624,a625,a626,a627,a628,a629,a630,a631,a632,a633,a634,a635,a636,a637,a638,a639,a640,a641,a642,a643
    ,a644,a645,a646,a647,a648,a649,a650,a651,a652,a653,a654,a655,a656,a657,a658,a659,a660,a661,a662,a663,a664,a665,a666,a667,a668,a669,a670,a671
    ,a672,a673,a674,a675,a676,a677,a678,a679,a680,a681,a682,a683,a684,a685,a686,a687,a688,a689,a690,a691,a692,a693,a694,a695,a696,a697,a698,a699
    ,a700,a701,a702,a703,a704,a705,a706,a707,a708,a709,a710,a711,a712,a713,a714,a715,a716,a717,a718,a719,a720,a721,a722,a723,a724,a725,a726,a727
    ,a728,a729,a730,a731,a732,a733,a734,a735,a736,a737,a738,a739,a740,a741,a742,a743,a744,a745,a746,a747,a748,a749,a750,a751,a752,a753,a754,a755
    ,a756,a757,a758,a759,a760,a761,a762,a763,a764,a765,a766,a767,a768,a769,a770,a771,a772,a773,a774,a775,a776,a777,a778,a779,a780,a781,a782,a783
    ,letter from hw_data_2 order by random() limit 100;""")
    
    input_nums = res.fetchall()

    network_obj = network(created_network)
 
    network_obj.train_network(input_nums, 1, 1000000, 0.05)

