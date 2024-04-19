import math

class CacheSimulator:
    def __init__(self, cache_size, block_size, memory_size):
        self.cache_size = cache_size
        self.block_size = block_size
        self.memory_size = memory_size
        self.num_blocks = cache_size // block_size
        self.cache = {index: {'tag': None, 'data': None} for index in range(self.num_blocks)}
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def access_memory(self, address):
        block_number = address // self.block_size
        index = block_number % self.num_blocks
        tag = block_number // self.num_blocks
        print("Address :",str('{:016b}'.format(address)))
        if self.cache[index]['tag'] == tag if index in self.cache else None:
            self.hits += 1
            print("Cache hit!")
            self.print_cache_state()
            return "hit"
        elif index in self.cache and self.cache[index]['tag'] is not None:
            self.evictions += 1
            self.misses += 1
            self.cache[index] = {'tag': tag, 'data': 'some data'}
            print("Cache miss! Evicting old block.")
            self.print_cache_state()
            return "miss"
        else:
            self.misses += 1
            self.cache[index] = {'tag': tag, 'data': 'some_data'}
            print("Cache miss! Writing new block")
            self.print_cache_state()
            return "miss"

    def print_cache_state(self):
        print("Current Cache State:")
        print("-" * 40)
        print("| {:<10} | {:<10} | {:<10} |".format("Index", "Tag", "Data"))
        print("-" * 40)
        for index, block in self.cache.items():
            tag = block['tag'] if block['tag'] is not None else "-"
            data = block['data'] if block['data'] is not None else "-"
            print("| {:<10} | {:<10} | {:<10} |".format(index, tag, data))
        print("-" * 40)
        print()
        print()


    def get_stats(self):
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            return "No accesses performed"
        hit_ratio = self.hits / total_accesses
        miss_ratio = self.misses / total_accesses
        return f"Total accesses: {total_accesses}, Hit ratio: {hit_ratio:.2f}, Miss ratio: {miss_ratio:.2f}"


def main():
    print("Cache Simulator Configuration")
    cache_size = int(input("Enter cache size (e.g., 32 for 32 words): "))
    memory_size = int(input("Enter memory size (e.g., 2048 for 2048 words): "))
    block_size = int(input("Enter block size: "))
    # block_size = 2 ** offset_bits
    offset_bits = int(math.log2(block_size))

    index_bits = int(math.log2(cache_size // block_size))
    total_address_bits = int(math.log2(memory_size))
    tag_bits = total_address_bits - index_bits - offset_bits

    print("\nCache configuration")
    print(f"Offset: {offset_bits} bits")
    print(f"Index bits: {index_bits} bits")
    print(f"Instruction Length = {total_address_bits} bits")
    print(f"Tag = {tag_bits} bits")
    # print(f"Block = {tag_bits + offset_bits} bits")

    simulator = CacheSimulator(cache_size, block_size, memory_size)

    simulator.print_cache_state()

    while True:
        address_input = input("Enter a memory address (or 'exit' to finish): ")
        if address_input.lower() == "exit":
            break

        if address_input.isdigit():
            simulator.access_memory(int(address_input)) 
        else:
            print("Invalid input. Please enter a valid number or 'exit'.")
    print(simulator.get_stats())


if __name__ == "__main__":
    main()
