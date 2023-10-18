from typing import Literal
from .cache import Cache


class L2Cache(Cache):
    def __init__(
        self,
        associativity,
        block_size,
        cache_size,
        replacement_policy,
        inclusion_property,
        next_level = None,
    ):
        super().__init__(
            associativity,
            block_size,
            cache_size,
            replacement_policy,
            inclusion_property,
            next_level,
        )

    # Usually called by upper level cache for write-back of a dirty block
    def write(self, address):
        tag, index = self.get_address_components(address)
        self.allocate_block(index, tag, address, is_dirty=True)
        self.write_hits += 1
