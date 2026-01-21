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
        except Exception as e:
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
):
    """
    List files in specified directory.

    Args:
        path (str): directory path to list files from
        recursive (bool): whether to list files recursively

    Returns:
        list: List of file paths in the directory
    """
    if not os.path.isdir(path):
        return {"error": f"Path {path} is not a directory"}

    if recursive:
        file_list = []
        for root, _, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    else:
        return os.listdir(path)


if __name__ == "__main__":
    mcp.run(transport="stdio")
