from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Initialize FastMCP server
mcp = FastMCP("basic-exec-cli-agent")


def format_output(returncode: int, stdout: str, stderr: str) -> str:
    """
    Format the output of a CLI command execution.

    Args:
        returncode (int): The return code of the executed command
        stdout (str): The standard output of the command
        stderr (str): The standard error of the command

    Returns:
        str: Formatted string with return code, stdout, and stderr
    """
    return f"RETURN CODE: {returncode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"


@mcp.tool()
def run_cli_command(
    command: str = Field(
        description="CLI command to execute. Supports shell commands with arguments."
    ),
):
    """
    Execute a CLI command and return structured output.

    Runs a shell command and returns the return code, standard output, and standard error
    in a structured format for easy parsing.

    Args:
        command (str): The CLI command to execute

    Returns:
        str: Formatted output containing return code, stdout, and stderr
    """
    import subprocess

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return format_output(result.returncode, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        return format_output(e.returncode, e.stdout, e.stderr)


if __name__ == "__main__":
    mcp.run(transport="stdio")
