"""User entity for MagicSquare domain."""

from dataclasses import dataclass, replace
from typing import Literal

InputMode = Literal["ui", "api", "cli"]
_ALLOWED_INPUT_MODES: tuple[str, ...] = ("ui", "api", "cli")


@dataclass(frozen=True, slots=True)
class User:
    """Represent a user in the entity layer.

    This entity keeps only pure domain data and validation logic.
    It does not depend on UI, framework, or infrastructure details.
    """

    user_id: str
    display_name: str
    preferred_input_mode: InputMode = "cli"
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate entity invariants after initialization."""
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")
        if not self.display_name.strip():
            raise ValueError("display_name must not be empty")
        if self.preferred_input_mode not in _ALLOWED_INPUT_MODES:
            raise ValueError(
                f"preferred_input_mode must be one of {_ALLOWED_INPUT_MODES}"
            )

    def rename(self, new_display_name: str) -> "User":
        """Return a new user with updated display name.

        Args:
            new_display_name: New display name for the user.

        Returns:
            User: A new immutable user instance.
        """
        if not new_display_name.strip():
            raise ValueError("display_name must not be empty")
        return replace(self, display_name=new_display_name)

    def deactivate(self) -> "User":
        """Return a new user marked as inactive.

        Returns:
            User: A new immutable user instance with inactive status.
        """
        return replace(self, is_active=False)

    def activate(self) -> "User":
        """Return a new user marked as active.

        Returns:
            User: A new immutable user instance with active status.
        """
        return replace(self, is_active=True)
