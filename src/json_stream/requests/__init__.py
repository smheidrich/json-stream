import io

import json_stream


class IterableStream(io.RawIOBase):
    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.remainder = None

    def readinto(self, buffer):
        try:
            chunk = self.remainder or next(self.iterator)
            length = min(len(buffer), len(chunk))
            buffer[:length], self.remainder = chunk[:length], chunk[length:]
            return length
        except StopIteration:
            return 0    # indicate EOF

    def readable(self):
        return True


def _to_file(response):
    return io.BufferedReader(IterableStream(response.iter_content()))


def load(response, persistent=False):
    return json_stream.load(_to_file(response), persistent=persistent)


def visit(response, visitor):
    return json_stream.visit(_to_file(response), visitor)
