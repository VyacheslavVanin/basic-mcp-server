from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional
import os

# Initialize FastMCP server
mcp = FastMCP("basic-read-files-agent")


@mcp.tool()
def read_file(
    path: str = Field(
        description="Path to file you want to read",
    ),
):
    """
    Return contents of file located at specified path.

    Args:
        path (str): path to file you want to read

    Returns:
        str: The contents of file requested
    """

    with open(path, "r") as f:
        return f.read()


@mcp.tool()
def read_multiple_files(
    paths: list[str] = Field(
        description="List of files you want to read",
    ),
):
    """
    Return dictionary with filenames as keys and contents of file as values.
    If failed to read file then value is None.

    Args:
        paths (list[str]): List of files you want to read

    Returns:
        dict[str, str|None]: The contents of file requested
    """
    ret = dict()
    for path in paths:
        try:
            with open(path, "r") as f:
                ret[path] = f.read()
        except Exception:
            ret[path] = None
    return ret


@mcp.tool()
def list_files(
    path: str = Field(
        description="Path to directory to list files from",
    ),
    recursive: Optional[bool] = Field(
        default=False, description="Whether to list files recursively"
    ),
    include_hidden: Optional[bool] = Field(
        default=False, description="Whether to include hidden files"
    ),
):
    """
    List files in specified directory.
    Args:
        path (str): Directory path to list files from.
        recursive (bool): Whether to list files recursively. Note: Be cautious when using this with large directories as it may significantly increase processing time and memory usage.
        include_hidden (bool): Whether to include hidden files. Note: This can capture too many files if applied to the project's root directory (e.g., '.env' or '.git' directories).
    Returns:
        list: List of file paths in the directory
    """
    if not os.path.isdir(path):
        return {"error": f"Path {path} is not a directory"}
    if recursive:
        file_list = []
        for root, dirnames, files in os.walk(path):
            # Filter out hidden directories unless include_hidden is True
            if not include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            for file in files:
                if include_hidden or not file.startswith('.'):
                    file_list.append(os.path.join(root, file))
        return file_list
    else:
        files = os.listdir(path)
        if not include_hidden:
            files = [f for f in files if not f.startswith('.')]
        return files
