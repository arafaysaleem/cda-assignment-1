from typing import List

from .cache import Cache


class CacheHeirarchy:
    def __init__(
        self, replacement_policy: int, inclusion_property: int, block_size: int
    ):
        self.cache_levels: List[Cache] = []
        self.replacement_policy = replacement_policy
        self.inclusion_property = inclusion_property
        self.block_size = block_size

    def create_cache(self, level: int, cache_size: int, associativity: int):
        cache = Cache(
            level=level,
            associativity=associativity,
            cache_size=cache_size,
            block_size=self.block_size,
            replacement_policy=self.replacement_policy,
            inclusion_property=self.inclusion_property,
        )
        if len(self.cache_levels) > 0:
            cache.prev_level = self.cache_levels[-1]
            self.cache_levels[-1].next_level = cache
        self.cache_levels.append(cache)

    def read(self, address: str):
        self.cache_levels[0].read(address)

    def write(self, address: str):
        self.cache_levels[0].write(address)

    def __str__(self) -> str:
        return "\n".join([str(cache) for cache in self.cache_levels])

    def __print_measurements(self):
        # Store the numbers in local variables
        num_l1_reads = self.cache_levels[0].reads
        num_l1_read_misses = self.cache_levels[0].read_misses
        num_l1_writes = self.cache_levels[0].writes
        num_l1_write_misses = self.cache_levels[0].write_misses
        l1_miss_rate = (num_l1_read_misses + num_l1_write_misses) / (num_l1_reads + num_l1_writes)
        num_l1_writebacks = self.cache_levels[0].write_backs
        num_l1_direct_writebacks = self.cache_levels[0].direct_write_backs
        total_memory_traffic = num_l1_read_misses + num_l1_write_misses + num_l1_writebacks

        # Print the simulation results
        print("===== Simulation results (raw) =====")
        print(f"a. number of L1 reads:        {num_l1_reads}")
        print(f"b. number of L1 read misses:  {num_l1_read_misses}")
        print(f"c. number of L1 writes:       {num_l1_writes}")
        print(f"d. number of L1 write misses: {num_l1_write_misses}")
        print(f"e. L1 miss rate:              {l1_miss_rate}")
        print(f"f. number of L1 writebacks:   {num_l1_writebacks}")

        num_l2_reads = 0
        num_l2_read_misses = 0
        num_l2_writes = 0
        num_l2_write_misses = 0
        l2_miss_rate = 0
        num_l2_writebacks = 0

        if len(self.cache_levels) > 1:
            num_l2_reads = self.cache_levels[1].reads
            num_l2_read_misses = self.cache_levels[1].read_misses
            num_l2_writes = self.cache_levels[1].writes
            num_l2_write_misses = self.cache_levels[1].write_misses
            l2_miss_rate = num_l2_read_misses / num_l2_reads
            num_l2_writebacks = self.cache_levels[1].write_backs
            total_memory_traffic = num_l2_read_misses + num_l2_write_misses + num_l2_writebacks
            if self.inclusion_property == 1:
                total_memory_traffic += num_l1_direct_writebacks

        print(f"g. number of L2 reads:        {num_l2_reads}")
        print(f"h. number of L2 read misses:  {num_l2_read_misses}")
        print(f"i. number of L2 writes:       {num_l2_writes}")
        print(f"j. number of L2 write misses: {num_l2_write_misses}")
        print(f"k. L2 miss rate:              {l2_miss_rate}")
        print(f"l. number of L2 writebacks:   {num_l2_writebacks}")
        print(f"m. total memory traffic:      {total_memory_traffic}")


    def print_results(self):
        print(self)
        self.__print_measurements()