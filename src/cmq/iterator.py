import contextlib
from atpbar.main import Atpbar, fetch_reporter, Report


class UnknownSizeIterator:

    def __init__(self, iterator):
        self.count = 0
        self.iterator = iterator

    def __iter__(self):
        for x in self.iterator:
            self.count += 1
            yield x

    def __len__(self):
        return self.count+1


class InfiniteAtpbar(Atpbar):
    """
    Atpbar with a custom reporter
    """

    def __iter__(self):
        with fetch_reporter() as reporter:
            if reporter is None:
                yield from self.iterable
                return
            self.reporter = reporter
            self.loop_complete = False
            self._report_start()
            with self._report_last():
                for i, e in enumerate(self.iterable):
                    yield e
                    self._done = i + 1
                    self.len_ = self._done + 1
                    self._report_progress()
                else:
                    self.loop_complete = True

    @contextlib.contextmanager
    def _report_last(self):
        try:
            yield
        finally:
            report = Report(
                task_id=self.id_,
                name=self.name,
                done=self._done,
                total=self._done,
                first=False,
                last=True,
            )
            self._submit(report)
