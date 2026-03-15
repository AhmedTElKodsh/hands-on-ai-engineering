"""
Command-line interface entrypoint.

Usage:
    python -m app [command]

Commands:
    serve   - Start the FastAPI server (default)
    health  - Check API health
    version - Show version
"""

import sys
import argparse
from pathlib import Path


def cmd_serve(args):
    """Start the FastAPI server."""
    import uvicorn
    from app.core.config import get_settings
    
    settings = get_settings()
    
    print(f"Starting {settings.app_name} v{settings.version}")
    print(f"Environment: {settings.app_env}")
    print(f"Host: {settings.api_host}:{settings.api_port}")
    print(f"Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )


def cmd_health(args):
    """Check API health."""
    import httpx
    
    from app.core.config import get_settings
    settings = get_settings()
    
    url = f"http://{settings.api_host}:{settings.api_port}/health"
    
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            print("✅ API is healthy")
            print(f"   App: {data.get('app', 'unknown')}")
            print(f"   Environment: {data.get('environment', 'unknown')}")
            return 0
    except httpx.HTTPError as e:
        print(f"❌ API health check failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def cmd_version(args):
    """Show version information."""
    from app.core.config import get_settings
    from app import __version__
    
    settings = get_settings()
    
    print(f"{settings.app_name}")
    print(f"Version: {settings.version}")
    print(f"Environment: {settings.app_env}")
    print(f"Python: {sys.version.split()[0]}")
    return 0


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="app",
        description="Layer 1 Phase 1 CLI"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI server")
    serve_parser.set_defaults(func=cmd_serve)
    
    # health command
    health_parser = subparsers.add_parser("health", help="Check API health")
    health_parser.set_defaults(func=cmd_health)
    
    # version command
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=cmd_version)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Default to serve if no command
    if args.command is None:
        args.command = "serve"
        args.func = cmd_serve
    
    # Execute command
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
