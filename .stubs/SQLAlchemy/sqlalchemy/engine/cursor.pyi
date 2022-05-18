"""
MIT License

Copyright (c) 2022-present japandotorg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import abc
from typing import Any

from ..util import memoized_property
from .result import Result, ResultMetaData
from .row import LegacyRow

MD_INDEX: int
MD_RESULT_MAP_INDEX: int
MD_OBJECTS: int
MD_LOOKUP_KEY: int
MD_RENDERED_NAME: int
MD_PROCESSOR: int
MD_UNTRANSLATED: int

class CursorResultMetaData(ResultMetaData):
    returns_rows: bool
    case_sensitive: Any
    def __init__(self, parent, cursor_description) -> None: ...

class LegacyCursorResultMetaData(CursorResultMetaData): ...

class ResultFetchStrategy:
    alternate_cursor_description: Any
    def soft_close(self, result, dbapi_cursor) -> None: ...
    def hard_close(self, result, dbapi_cursor) -> None: ...
    def yield_per(self, result, dbapi_cursor, num) -> None: ...
    def fetchone(self, result, dbapi_cursor, hard_close: bool = ...) -> None: ...
    def fetchmany(self, result, dbapi_cursor, size: Any | None = ...) -> None: ...
    def fetchall(self, result) -> None: ...
    def handle_exception(self, result, dbapi_cursor, err) -> None: ...

class NoCursorFetchStrategy(ResultFetchStrategy):
    def soft_close(self, result, dbapi_cursor) -> None: ...
    def hard_close(self, result, dbapi_cursor) -> None: ...
    def fetchone(self, result, dbapi_cursor, hard_close: bool = ...): ...
    def fetchmany(self, result, dbapi_cursor, size: Any | None = ...): ...
    def fetchall(self, result, dbapi_cursor): ...

class NoCursorDQLFetchStrategy(NoCursorFetchStrategy): ...
class NoCursorDMLFetchStrategy(NoCursorFetchStrategy): ...

class CursorFetchStrategy(ResultFetchStrategy):
    def soft_close(self, result, dbapi_cursor) -> None: ...
    def hard_close(self, result, dbapi_cursor) -> None: ...
    def handle_exception(self, result, dbapi_cursor, err) -> None: ...
    def yield_per(self, result, dbapi_cursor, num) -> None: ...
    def fetchone(self, result, dbapi_cursor, hard_close: bool = ...): ...
    def fetchmany(self, result, dbapi_cursor, size: Any | None = ...): ...
    def fetchall(self, result, dbapi_cursor): ...

class BufferedRowCursorFetchStrategy(CursorFetchStrategy):
    def __init__(self, dbapi_cursor, execution_options, growth_factor: int = ..., initial_buffer: Any | None = ...) -> None: ...
    @classmethod
    def create(cls, result): ...
    def yield_per(self, result, dbapi_cursor, num) -> None: ...
    def soft_close(self, result, dbapi_cursor) -> None: ...
    def hard_close(self, result, dbapi_cursor) -> None: ...
    def fetchone(self, result, dbapi_cursor, hard_close: bool = ...): ...
    def fetchmany(self, result, dbapi_cursor, size: Any | None = ...): ...
    def fetchall(self, result, dbapi_cursor): ...

class FullyBufferedCursorFetchStrategy(CursorFetchStrategy):
    alternate_cursor_description: Any
    def __init__(self, dbapi_cursor, alternate_description: Any | None = ..., initial_buffer: Any | None = ...) -> None: ...
    def yield_per(self, result, dbapi_cursor, num) -> None: ...
    def soft_close(self, result, dbapi_cursor) -> None: ...
    def hard_close(self, result, dbapi_cursor) -> None: ...
    def fetchone(self, result, dbapi_cursor, hard_close: bool = ...): ...
    def fetchmany(self, result, dbapi_cursor, size: Any | None = ...): ...
    def fetchall(self, result, dbapi_cursor): ...

class _NoResultMetaData(ResultMetaData):
    returns_rows: bool
    @property
    def keys(self) -> None: ...

class _LegacyNoResultMetaData(_NoResultMetaData):
    @property
    def keys(self): ...

class BaseCursorResult:
    out_parameters: Any
    closed: bool
    context: Any
    dialect: Any
    cursor: Any
    cursor_strategy: Any
    connection: Any
    def __init__(self, context, cursor_strategy, cursor_description): ...
    @property
    def inserted_primary_key_rows(self): ...
    @property
    def inserted_primary_key(self): ...
    def last_updated_params(self): ...
    def last_inserted_params(self): ...
    @property
    def returned_defaults_rows(self): ...
    @property
    def returned_defaults(self): ...
    def lastrow_has_defaults(self): ...
    def postfetch_cols(self): ...
    def prefetch_cols(self): ...
    def supports_sane_rowcount(self): ...
    def supports_sane_multi_rowcount(self): ...
    @memoized_property
    def rowcount(self): ...
    @property
    def lastrowid(self): ...
    @property
    def returns_rows(self): ...
    @property
    def is_insert(self): ...

class CursorResult(BaseCursorResult, Result):
    def merge(self, *others): ...
    def close(self) -> None: ...

class LegacyCursorResult(CursorResult):
    def close(self) -> None: ...

ResultProxy = LegacyCursorResult

class BufferedRowResultProxy(ResultProxy): ...
class FullyBufferedResultProxy(ResultProxy): ...
class BufferedColumnRow(LegacyRow, metaclass=abc.ABCMeta): ...
class BufferedColumnResultProxy(ResultProxy): ...