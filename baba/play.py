"""
Main entry point for playing Baba Is You.

Provides a simple interface to play the game interactively.
For AI agents, use the scripts in the agents/ directory.
"""

import argparse
import sys

from .agent import UserAgent
from .envs import create_environment, list_environments


def play(
    env_name: str = "simple",
    render: bool = True,
    cell_size: int = 48,
    fps: int = 30,
    verbose: bool = True,
) -> dict:
    """
    Play Baba Is You interactively.

    Args:
        env_name: Name of the environment to play
        render: Whether to render visually
        cell_size: Size of each cell in pixels
        fps: Frames per second for rendering
        verbose: Whether to print information

    Returns:
        Dictionary with episode statistics
    """
    # Create environment
    env = create_environment(env_name)
    if not env:
        print(f"Environment '{env_name}' not found.")
        print(f"Available environments: {', '.join(list_environments())}")
        sys.exit(1)

    # Create user agent for interactive play
    agent = UserAgent()

    # Play episode using new Agent API
    stats = agent.play_episode(
        env=env,
        render=render,
        cell_size=cell_size,
        fps=fps,
        verbose=verbose,
    )

    return stats


def main():
    """Command-line interface for playing Baba Is You."""
    parser = argparse.ArgumentParser(
        description="Play Baba Is You interactively",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Play interactively (default)
  pixi run play

  # Play specific environment
  pixi run play --env push_puzzle

  # Play with larger cells
  pixi run play --cell-size 64

For AI agents, see the agents/ directory:
  python agents/random.py simple
  python agents/claude-code.py simple
""",
    )

    parser.add_argument(
        "--env",
        default="simple",
        help="Environment to play (default: simple)",
    )

    parser.add_argument(
        "--cell-size",
        type=int,
        default=48,
        help="Size of each cell in pixels (default: 48)",
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)",
    )

    parser.add_argument(
        "--list-envs",
        action="store_true",
        help="List available environments and exit",
    )

    args = parser.parse_args()

    # Handle list environments
    if args.list_envs:
        print("Available environments:")
        for env_name in sorted(list_environments()):
            print(f"  - {env_name}")
        return 0

    # Play the game
    try:
        play(
            env_name=args.env,
            render=True,
            cell_size=args.cell_size,
            fps=args.fps,
            verbose=True,
        )
    except KeyboardInterrupt:
        print("\nGame interrupted by user")

    return 0


if __name__ == "__main__":
    sys.exit(main())
