from _typeshed import Incomplete
from atpbar.main import Atpbar

class UnknownSizeIterator:
    count: int
    iterator: Incomplete
    def __init__(self, iterator) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...

class InfiniteAtpbar(Atpbar):
    reporter: Incomplete
    loop_complete: bool
    len_: Incomplete
    def __iter__(self): ...
