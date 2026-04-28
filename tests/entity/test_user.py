"""Tests for the User entity in ECB entity layer."""

import pytest

from magicsquare.entity.user import User


def test_user_creation_with_valid_values() -> None:
    """Create user with valid fields."""
    # Arrange
    user_id = "user-1004"
    display_name = "Magic Solver"

    # Act
    user = User(user_id=user_id, display_name=display_name, preferred_input_mode="cli")

    # Assert
    assert user.user_id == user_id
    assert user.display_name == display_name
    assert user.preferred_input_mode == "cli"
    assert user.is_active is True


def test_user_creation_raises_for_blank_user_id() -> None:
    """Reject blank user_id."""
    # Arrange
    blank_user_id = "   "

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must not be empty"):
        User(user_id=blank_user_id, display_name="Valid Name")


def test_user_creation_raises_for_blank_display_name() -> None:
    """Reject blank display_name."""
    # Arrange
    blank_display_name = ""

    # Act / Assert
    with pytest.raises(ValueError, match="display_name must not be empty"):
        User(user_id="user-1004", display_name=blank_display_name)


def test_user_creation_raises_for_invalid_input_mode() -> None:
    """Reject unsupported preferred_input_mode."""
    # Arrange
    invalid_mode = "console"

    # Act / Assert
    with pytest.raises(ValueError, match="preferred_input_mode must be one of"):
        User(user_id="user-1004", display_name="Magic Solver", preferred_input_mode=invalid_mode)


def test_rename_returns_new_user_without_mutating_original() -> None:
    """Return new immutable instance when renamed."""
    # Arrange
    user = User(user_id="user-1004", display_name="Old Name")

    # Act
    renamed_user = user.rename("New Name")

    # Assert
    assert user.display_name == "Old Name"
    assert renamed_user.display_name == "New Name"
    assert renamed_user.user_id == user.user_id
    assert renamed_user.preferred_input_mode == user.preferred_input_mode


def test_deactivate_and_activate() -> None:
    """Toggle active status with immutable updates."""
    # Arrange
    user = User(user_id="user-1004", display_name="Magic Solver")

    # Act
    inactive_user = user.deactivate()
    reactivated_user = inactive_user.activate()

    # Assert
    assert user.is_active is True
    assert inactive_user.is_active is False
    assert reactivated_user.is_active is True
