import sys

from src.caches.cache_heirarchy import CacheHeirarchy


class Simulator:
    def __init__(
        self,
        block_size: int,
        l1_size: int,
        l1_assoc: int,
        l2_size: int,
        l2_assoc: int,
        replacement_policy: int,
        inclusion_property: int,
        trace_file: str,
    ):
        self.block_size = block_size
        self.l1_size = l1_size
        self.l1_assoc = l1_assoc
        self.l2_size = l2_size
        self.l2_assoc = l2_assoc
        self.replacement_policy = replacement_policy
        self.inclusion_property = inclusion_property
        self.trace_file = trace_file

    def create_caches(self):
        # Create the cache heirarchy
        self.cache_heirarchy = CacheHeirarchy(
            replacement_policy=self.replacement_policy,
            inclusion_property=self.inclusion_property,
            block_size=self.block_size,
        )
        self.cache_heirarchy.create_cache(
            level=1, cache_size=self.l1_size, associativity=self.l1_assoc
        )
        if self.l2_size > 0:
            self.cache_heirarchy.create_cache(
                level=2, cache_size=self.l2_size, associativity=self.l2_assoc
            )

    def run(self):
        # Read the trace file
        with open(self.trace_file, "r") as file:
            for line in file:
                (
                    operation,
                    address,
                ) = line.split()  # split the line into operation and address

                if operation == "r":
                    self.cache_heirarchy.read(address)
                elif operation == "w":
                    self.cache_heirarchy.write(address)

    def __print_configuration(self):
        print("===== Simulator configuration =====")
        print(f"BLOCKSIZE:             {self.block_size}")
        print(f"L1_SIZE:               {self.l1_size}")
        print(f"L1_ASSOC:              {self.l1_assoc}")
        print(f"L2_SIZE:               {self.l2_size}")
        print(f"L2_ASSOC:              {self.l2_assoc}")
        print(
            f"REPLACEMENT POLICY:    {'LRU' if self.replacement_policy == 0 else 'FIFO'}"
        )
        print(
            f"INCLUSION PROPERTY:    {'non-inclusive' if self.inclusion_property == 0 else 'inclusive'}"
        )
        print(f"trace_file:            {self.trace_file}")

    def print_results(self):
        self.__print_configuration()
        self.cache_heirarchy.print_results()
