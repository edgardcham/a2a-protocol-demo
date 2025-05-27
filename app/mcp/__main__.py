#!/usr/bin/env python3
"""
MCP Server startup script for Travel Tools
"""

if __name__ == "__main__":
    import os
    import sys

    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Import and run the FastMCP server
    from server import mcp

    print("Starting Travel Tools MCP Server...")
    print("Available tools: get_flights, get_stays")
    print("Server ready for connections...")

    # This will start the FastMCP server in stdio mode
    # which is what ADK agents expect
    mcp.run()
