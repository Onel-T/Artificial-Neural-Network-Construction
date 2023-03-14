class node:
    def __init__(self, connections):
        self.connection = connections
        self.collector = 0.0

# Returns list of numbers from from csv
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
    

if __name__ == '__main__':
    nodes_per_layer = strip_csv("network.txt")
    input_nums = strip_csv("input.txt")

