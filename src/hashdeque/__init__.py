"""hashdeque: a string deque that maintains an O(1) rolling hash of its contents.

Public API:

* :class:`HashDeque` - concrete polynomial double rolling-hash deque.
* :class:`BaseHashDeque` - abstract base class / extension contract.
* :class:`HashParams` and :data:`DEFAULT_PARAMS` - hash configuration.
"""

from __future__ import annotations

from .base import BaseHashDeque
from .deque import HashDeque
from .params import DEFAULT_PARAMS, HashParams

__version__ = "0.0.3"

__all__ = [
    "HashDeque",
    "BaseHashDeque",
    "HashParams",
    "DEFAULT_PARAMS",
    "__version__",
]
