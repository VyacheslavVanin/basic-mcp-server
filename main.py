from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional
import os

# Initialize FastMCP server
mcp = FastMCP("basic-agent")


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
