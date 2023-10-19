from typing import cast
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Block:
    tag: str | None = None
    address: str | None = None
    is_dirty: bool = False
    is_valid: bool = False
    sequence_number: int = 0

    def copy_with(self, **kwargs):
        return replace(self, **kwargs)
    
    def __str__(self):
        tag = cast(str, self.tag)
        return f"{tag[2:]} {"D" if self.is_dirty else " "}"
