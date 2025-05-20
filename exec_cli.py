from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional
import os

# Initialize FastMCP server
mcp = FastMCP("basic-exec-cli-agent")


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


if __name__ == "__main__":
    mcp.run(transport="stdio")
