from __future__ import annotations
from abc import ABC, abstractmethod
from math import log2
from typing import List, Literal
from blocks.block import Block

ADDRESS_BITS = 32


class Cache(ABC):
    def __init__(
        self,
        associativity: int,
        block_size: int,
        cache_size: int,
        replacement_policy: int,
        inclusion_property: int,
        next_level: Cache | None = None,
        prev_level: Cache | None = None,
    ):
        self.associativity = associativity
        self.block_size = block_size
        self.cache_size = cache_size
        self.sets = cache_size // (associativity * block_size)
        self.index_bits = log2(self.sets)
        self.tag_bits = ADDRESS_BITS - self.index_bits - log2(block_size)
        self.blocks: List[List[Block]] = [
            [Block()] * associativity for _ in range(self.sets)
        ]
        self.replacement_policy = replacement_policy
        self.inclusion_property = inclusion_property
        self.sequence_counter = 0
        self.read_hits = 0
        self.read_misses = 0
        self.write_hits = 0
        self.write_misses = 0
        self.write_backs = 0
        self.next_level = next_level
        self.prev_level = prev_level

    @abstractmethod
    def write(self, address: str):
        pass

    def read(self, address):
        tag, set_index = self.get_address_components(address)
        result = self.get_block(set_index, tag)
        if result is not None:
            block, block_index = result
            self.read_hit_block(set_index, block_index, block)
        else:
            self.read_misses += 1
            if self.next_level is not None:
                self.next_level.read(address)
            # else: read from memory. We skip this bcz we don't want actual I/O

            # By now, the block is assumed to be read from next level or memory
            # Finally, allocate the block
            self.allocate_block(set_index, tag, address)

    def read_hit_block(self, set_index: int, block_index: int, block: Block) -> None:
        self.blocks[set_index][block_index] = block.copy_with(
            sequence_number=self.sequence_counter
        )
        self.read_hits += 1
        if self.replacement_policy == 0:  # only for LRU
            self.sequence_counter += 1

    def write_hit_block(self, set_index: int, block_index: int, block: Block) -> None:
        self.blocks[set_index][block_index] = block.copy_with(
            sequence_number=self.sequence_counter,
            is_dirty=True
        )
        self.write_hits += 1
        if self.replacement_policy == 0:  # only for LRU
            self.sequence_counter += 1

    def write_back(self, address) -> None:
        self.write_backs += 1
        if self.next_level is not None:
            self.next_level.write(address)
        # else: write to memory. We skip this bcz we don't want actual I/O

    def evict(self, set_index: int, address: str) -> tuple[Block, int]:
        ways = self.blocks[set_index]
        # Both replacement policies use the same concept (kick lowest sequence number), hence we don't do if-else
        # if self.replacement_policy == 0 or self.replacement_policy == 1:
        victim_block_index = 0
        victim_block = ways[victim_block_index]
        for i, block in enumerate(ways):
            if block.is_valid is False:
                if block.is_dirty:
                    self.write_back(address)
                victim_block = block
                victim_block_index = i
                break
            if block.sequence_number < victim_block.sequence_number:
                victim_block = block
                victim_block_index = i

        if victim_block.is_dirty:
            self.write_back(address)
        return victim_block, victim_block_index

    def allocate_block(
        self, set_index: int, tag: str, address: str, is_dirty=False
    ) -> None:
        _, block_index = self.evict(set_index, address)
        new_block = Block(
            tag=tag,
            address=address,
            is_valid=True,
            is_dirty=is_dirty,
            sequence_number=self.sequence_counter,
        )
        self.blocks[set_index][block_index] = new_block
        self.sequence_counter += 1

    def get_block(self, set_index: int, tag: str) -> tuple[Block, int] | None:
        ways = self.blocks[set_index]
        for i, block in enumerate(ways):
            if block.tag == tag:
                return block, i
        return None

    def get_address_components(self, address: str) -> tuple[str, int]:
        # Zero-pad the hex address to address bits
        address = address.zfill(ADDRESS_BITS // 4)

        # Convert the address to binary
        binary_address = bin(int(address, 16))[2:].zfill(ADDRESS_BITS)

        # Extract the tag and index from the binary address
        tag = binary_address[: self.tag_bits]
        index = binary_address[self.tag_bits : self.tag_bits + self.index_bits]

        # Convert the tag back to hexadecimal
        tag = hex(int(tag, 2))

        return tag, int(index)
