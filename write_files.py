from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional
import os


def validate_path(path: str) -> tuple[bool, str]:
    """
    Validates that the path is absolute and does not contain '..' symbols.

    Args:
        path (str): Path to validate

    Returns:
        tuple[bool, str]: (is_valid, error_message_if_invalid)
    """
    # Check if path is absolute
    if not os.path.isabs(path):
        return (
            False,
            f"Error: Path '{path}' is not absolute. Only absolute paths are allowed.",
        )

    # Normalize the path and check for '..'
    normalized_path = os.path.normpath(path)
    if ".." in normalized_path.split(os.sep):
        return (
            False,
            f"Error: Path '{path}' contains '..' symbols which are not allowed.",
        )

    return True, ""


# Initialize FastMCP server
mcp = FastMCP("basic-write-files-agent")


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

    # Validate the path
    is_valid, error_msg = validate_path(path)
    if not is_valid:
        return error_msg

    try:
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return str(e)
    return "Success"


@mcp.tool()
def write_multiple_files(
    files: list[dict] = Field(
        description="List of files to write, each with 'path' and 'content' keys"
    ),
):
    """
    Write contents to multiple files. Each file will be overwritten.
    Use when you need to create or overwrite multiple files at once.
    Args:
        files (list[dict]): List of files to write, each with 'path' and 'content' keys. Example: [{"path": "a.txt", "content": "aaaaaa"}, {"path": "b.c", "content": "int main(){}"}]
    Returns:
        dict[str, str]: The status of the execution for each file: "Success" or error message.
    """
    results = {}
    for file_info in files:
        path = file_info["path"]
        content = file_info["content"]

        # Validate the path
        is_valid, error_msg = validate_path(path)
        if not is_valid:
            results[path] = error_msg
            continue

        try:
            directory = os.path.dirname(path)
            os.makedirs(directory, exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            results[path] = "Success"
        except Exception as e:
            results[path] = str(e)
    return results


@mcp.tool()
def edit_files(
    path: str = Field(
        description="Path to file to edit",
    ),
    match: str = Field(
        description="The string in file with EXACT fragment (with all spaces, tabs and new lines) of text that must be substituted or deleted. Can not be empty string",
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
        match (str): the string in file with EXACT fragment (with all spaces, tabs and new lines) of text that must be substituted or deleted. Can not be empty string.
        substitute (str): the string that must be placed instead of 'match'

    Returns:
         The status of the execution: "Success" if successful, or the error text in case of problems.
    """

    if not match:
        return "Error: 'match' argument cannot be empty string. Provide correct part of file."

    # Validate the path
    is_valid, error_msg = validate_path(path)
    if not is_valid:
        return error_msg

    try:
        with open(path, "r+") as f:
            content = f.read()
            if content.find(match) == -1:
                return "Error: match not found in file contents"
            new_content = content.replace(match, substitute, 1)
            f.seek(0)
            f.write(new_content)
            f.truncate()
    except Exception as e:
        return f"Error: {str(e)}, file not edited"
    return "Success"


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

    # Validate the path
    is_valid, error_msg = validate_path(path)
    if not is_valid:
        return error_msg

    try:
        os.makedirs(path, exist_ok=True)
        return "Success"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    mcp.run(transport="stdio")
