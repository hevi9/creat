# """ mk action base objects. """
#
# import os
# from abc import abstractmethod
# from contextlib import contextmanager
# from pathlib import Path
# from typing import Any, Iterable, Mapping, Optional
#
# from creat.index import Index
# from creat.items import Item, Runnable
# from creat.source import Source
#
#
# class Action(Item, Runnable):
#     """Base implementation for make items."""
#
#     @contextmanager
#     def _run_context(self):
#         if self.cd:
#             cwd_old = Path.cwd()
#             try:
#                 os.chdir(self.cd)
#                 yield self.cd, self.env
#             finally:
#                 os.chdir(cwd_old)
#         else:
#             yield None, self.env
#
#     @abstractmethod
#     def run(self, context: Mapping[str, Any]) -> None:
#         pass
