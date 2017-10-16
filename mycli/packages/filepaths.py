# -*- coding: utf-8
import os

def list_path(root_dir):
    """List directory if exists.

    :param dir: str
    :return: list

    """
    # Let empty path represent the current directory
    if not root_dir:
        root_dir = os.curdir
    # Return nothing if not a directory
    if not os.path.isdir(root_dir):
        return []

    # Append a path separator to all entries that are directories
    dir_entries = os.listdir(root_dir)
    for index, entry in enumerate(dir_entries):
        if os.path.isdir(os.path.join(root_dir, entry)):
            dir_entries[index] = entry + os.sep

    return dir_entries


def complete_path(curr_dir, last_dir):
    """Return the path to complete that matches the last entered component.

    If the last entered component is ~, expanded path would not
    match, so return all of the available paths.

    :param curr_dir: str
    :param last_dir: str
    :return: str

    """
    if not last_dir or curr_dir.startswith(last_dir):
        return curr_dir
    elif last_dir == '~':
        return os.path.join(last_dir, curr_dir)


def parse_path(root_dir):
    """Split path into head and last component for the completer.

    Also return position where last component starts.

    :param root_dir: str path
    :return: tuple of (string, string, int)

    """
    base_dir, last_dir, position = '', '', 0
    if root_dir:
        base_dir, last_dir = os.path.split(root_dir)
        position = -len(last_dir) if last_dir else 0
    return base_dir, last_dir, position


def suggest_path(root_dir):
    """Suggest multiple paths given a partially completed path. The provided
    path may contain user environment variables and home directory symbols.

    If a path is not specified, it is assumed that the suggestions should come
    from the current working directory.

    :param root_dir: string: directory to list
    :return: list

    """
    # Expand user path and all environment variables
    expanded_path = apply(root_dir, os.path.expanduser, os.path.expandvars)
    file_path, basename = os.path.split(expanded_path)

    # There won't be a basename if the provided path ends with a path separator
    if not basename:
        # Only show the files in the path that aren't hidden
        filter_func = lambda entry: not entry.startswith('.')
    else:
        # Use basename to filter suggestions
        filter_func = lambda entry: entry.startswith(basename)

    return filter(filter_func, list_path(file_path))


def dir_path_exists(path):
    """Check if the directory path exists for a given file.

    For example, for a file /home/user/.cache/mycli/log, check if
    /home/user/.cache/mycli exists.

    :param str path: The file path.
    :return: Whether or not the directory path exists.

    """
    return os.path.exists(os.path.dirname(path))


def apply(value, *functions):
    """Returns the result of applying a series of functions to a value.

    :param Any value: The value to apply functions to
    :param (Any) -> Any functions: A collection of functions to apply to value
    :return Any: The result of applying all functions to value
    """
    for transform in functions:
        value = transform(value)
    return value
