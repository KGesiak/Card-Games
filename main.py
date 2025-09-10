# ============================================================================
# MAIN.PY - Entry point
# ============================================================================
"""Main entry point for the Macau card game."""

from Game_Macau import Game_Macau

def main() -> None:
    """
    Main function that initializes and starts the Macau card game.
    """
    game = Game_Macau()
    game.Start()


if __name__ == "__main__":
    main()
