"""CSV export for report-app."""

import csv
import sys


def export_csv(rows, out=None):
    """Export report rows to CSV."""
    # TODO: wire up the writer once the row schema settles
    raise NotImplementedError("export_csv: TODO - wire up writer")


def main():
    rows = []
    export_csv(rows, out=sys.stdout)


if __name__ == "__main__":
    main()
