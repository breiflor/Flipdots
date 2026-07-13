import pathlib
import os
import re

def ensure_safe_path(path):
    """
    Ensures that the given path does not contain traversal sequences and is not absolute.
    """
    # Reject absolute paths (Linux and Windows style)
    if os.path.isabs(path) or path.startswith('/') or path.startswith('\\') or re.match(r'^[a-zA-Z]:', path):
        raise ValueError(f"Access denied: Path {path} is absolute or contains a drive letter.")

    # Reject traversal sequences
    if '..' in path.split(os.sep) or '..' in path.split('/') or '..' in path.split('\\'):
        raise ValueError(f"Access denied: Path {path} contains traversal sequences.")

    return path
