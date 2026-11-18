from _typeshed import Incomplete
from typing import Any
from atpbar.main import Atpbar as Atpbar

class UnknownSizeIterator:
    count: int
    iterator: Incomplete
    def __init__(self, iterator: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def __len__(self) -> int: ...

class InfiniteAtpbar(Atpbar):
    reporter: Incomplete
    loop_complete: bool
    len_: Incomplete
    def __iter__(self) -> Any: ...
