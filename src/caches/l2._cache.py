from typing import Literal
from .cache import Cache


class L2Cache(Cache):
    def __init__(
        self,
        associativity: int,
        block_size: int,
        cache_size: int,
        replacement_policy: Literal[0, 1],
        inclusion_policy: Literal[0, 1],
        next_level: Cache | None = None,
    ):
        super().__init__(
            associativity,
            block_size,
            cache_size,
            replacement_policy,
            inclusion_policy,
            next_level,
        )

    # Usually called by upper level cache for write-back of a dirty block
    def write(self, address):
        tag, index = self.get_address_components(address)
        self.allocate_block(index, tag, address, is_dirty=True)
        self.write_hits += 1
