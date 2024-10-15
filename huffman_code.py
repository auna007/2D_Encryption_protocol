from collections import defaultdict
import heapq

def huffman_encoding(dna_string):
    # Step 1: Obtain the frequency of A, G, C, T
    frequency = defaultdict(int)
    for char in dna_string:
        frequency[char] += 1
    
    # Step 2: Arrange characters in ascending order along with weights
    priority_queue = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(priority_queue)

    # Step 3 & 4: Build the Huffman Tree
    while len(priority_queue) > 1:
        low1 = heapq.heappop(priority_queue)
        low2 = heapq.heappop(priority_queue)
        for pair in low1[1:]:
            pair[1] = '0' + pair[1]
        for pair in low2[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(priority_queue, [low1[0] + low2[0]] + low1[1:] + low2[1:])

    # Step 6: Obtain binary sequence for A, G, C, T
    huffman_tree = priority_queue[0][1:]  # Get the characters with their codes
    huffman_codes = {char: code for char, code in huffman_tree}
    
    return huffman_codes

# Example usage
dna_string = "awwaliliyasu@gmail.com"
codes = huffman_encoding(dna_string)
print("Huffman Codes:")
for char, code in codes.items():
    print(f"{char}: {code}")
