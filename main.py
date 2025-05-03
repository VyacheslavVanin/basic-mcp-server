from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional
import os

# Initialize FastMCP server
mcp = FastMCP("basic-agent")


@mcp.tool()
def write_whole_file(
    path: str = Field(
        description="Path to file you want to read",
    ),
    content: str = Field(
        description="Contents you want to write",
    ),
):
    """
    Write contents to specified file. The whole file will be overwriten.
    Use when you need to create or overwrite existing file.
    Prefer use of edit_file if you need to make small changes.

    Args:
        path (str): path to file you want to write
        content (str): contents you want to write to file

    Returns:
         The status of the execution: "Success" if successful, or the error text in case of problems.
    """

    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return str(e)
    return "Success"


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


@mcp.tool()
def edit_files(
    path: str = Field(
        description="Path to file to edit",
    ),
    match: str = Field(
        description="The string in file with EXACT fragment (with all spaces, tabs and new lines) of text that must be substituted or deleted",
    ),
    substitute: str = Field(
        description="The string that must be placed instead of 'match'",
    ),
):
    """
    Edit specified file by replacing the 'match' string with 'substitute'.
    Use this method when you need to make smaller edits to a file without overwriting the entire file.
    Prefer to make smaller edits to avoid losing any existing data or functionality.

    Args:
        path (str): path to file to edit
        match (str): the string in file with EXACT fragment (with all spaces, tabs and new lines) of text that must be substituted or deleted
        substitute (str): the string that must be placed instead of 'match'

    Returns:
         The status of the execution: "Success" if successful, or the error text in case of problems.
    """

    try:
        with open(path, "r+") as f:
            content = f.read()
            new_content = content.replace(match, substitute)
            f.seek(0)
            f.write(new_content)
            f.truncate()
    except Exception as e:
        return f"Error: {str(e)}"
    return "Success"


@mcp.tool()
def run_cli_command(command: str = Field(description="CLI command to run")):
    """
    Run a CLI command.

    Args:
        command (str): The CLI command to run

    Returns:
        str: The output of the command or an error message
    """
    import subprocess

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


@mcp.tool()
def create_directory(
    path: str = Field(
        description="Path to directory you want to create",
    ),
):
    """
    Create a directory at the specified path.

    Args:
        path (str): path to directory you want to create

    Returns:
        str: The status of the execution: "Success" if successful, or the error text in case of problems.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return "Success"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run(transport="stdio")
