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

from typing import Any

from . import plugin_base

has_xdist: bool
py2k: Any

def pytest_addoption(parser) -> None: ...
def pytest_configure(config) -> None: ...

DUMP_PYANNOTATE: bool

def collect_types_fixture() -> None: ...
def pytest_sessionstart(session) -> None: ...
def pytest_sessionfinish(session) -> None: ...
def pytest_collection_finish(session): ...
def pytest_configure_node(node) -> None: ...
def pytest_testnodedown(node, error) -> None: ...
def pytest_collection_modifyitems(session, config, items): ...
def pytest_pycollect_makeitem(collector, name, obj): ...
def pytest_runtest_setup(item) -> None: ...
def pytest_runtest_teardown(item, nextitem) -> None: ...
def pytest_runtest_call(item) -> None: ...
def pytest_runtest_logreport(report) -> None: ...
def setup_class_methods(request) -> None: ...
def setup_test_methods(request) -> None: ...
def getargspec(fn): ...

class PytestFixtureFunctions(plugin_base.FixtureFunctions):
    def skip_test_exception(self, *arg, **kw): ...
    def mark_base_test_class(self): ...
    def combinations(self, *arg_sets, **kw): ...
    def param_ident(self, *parameters): ...
    def fixture(self, *arg, **kw): ...
    def get_current_test_name(self): ...
    def async_test(self, fn): ...