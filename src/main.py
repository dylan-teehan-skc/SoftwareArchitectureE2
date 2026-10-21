import sys
from functools import partial
from pathlib import Path

from app import EvaApp
from console import ConsoleInput, ConsoleOutput
from eva_data import load_evas
from plot import save_and_show_cumulative

PLOT_PATH = (
    Path(__file__).resolve().parent.parent / "output" / "cumulative_duration.png"
)


def main():
    plot = partial(save_and_show_cumulative, path=PLOT_PATH)
    try:
        EvaApp(ConsoleInput(), ConsoleOutput(), load_evas, plot).run()
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
