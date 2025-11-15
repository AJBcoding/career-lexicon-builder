from pathlib import Path
from typing import Optional
from fastapi import HTTPException


def validate_file_path(
    base_dir: Path,
    requested_path: str,
    allow_dirs: bool = False
) -> Path:
    """
    Validate that requested_path stays within base_dir.
    Prevents path traversal attacks.

    Args:
        base_dir: The safe base directory
        requested_path: User-supplied path (e.g., filename)
        allow_dirs: If True, accept directory traversal. If False, strip directories.

    Returns:
        Safe Path object that is guaranteed to be within base_dir

    Raises:
        HTTPException: If path traversal attempt detected
    """
    # If allow_dirs is False, use only the filename
    if not allow_dirs:
        requested_path = Path(requested_path).name

    # Resolve paths to absolute
    base_resolved = base_dir.resolve()
    requested_resolved = (base_dir / requested_path).resolve()

    # Check if requested path is within base directory
    try:
        requested_resolved.relative_to(base_resolved)
    except ValueError:
        # Path is outside base_dir
        raise HTTPException(
            status_code=403,
            detail="Access to this path is not allowed"
        )

    return requested_resolved
