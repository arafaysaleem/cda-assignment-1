from typing import Literal
from .cache import Cache


class L1Cache(Cache):
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

    def write(self, address):
        tag, index = self.get_address_components(address)
        result = self.get_block(index, tag)
        if result is not None:
            block, block_index = result
            # mark the block as dirty
            self.write_hit_block(index, block_index, block.copy_with(is_dirty=True))
        else:
            self.write_misses += 1
            if self.next_level is not None:
                # Reading from next level because of WBWA policy
                self.next_level.read(address)
            # else: read from memory. We skip this bcz we don't want actual I/O

            # By now, the block is assumed to be read from next level or memory
            # Finally, allocate the block
            self.allocate_block(index, tag, address, is_dirty=True)
