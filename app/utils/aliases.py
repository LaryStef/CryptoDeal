from typing import TypeAlias


RESTError: TypeAlias = tuple[int, dict[str, dict[str, str]]]
