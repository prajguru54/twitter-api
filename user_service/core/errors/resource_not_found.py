from typing import Any, Type


class ResourceNotFoundException(Exception):
    def __init__(self, type: Type, pk: Any) -> None:
        self.message = f"Resource for {type.__name__} with pk=({pk}) not found"
        self.code = "RESOURCE_NOT_FOUND"
        super().__init__(self.message)
