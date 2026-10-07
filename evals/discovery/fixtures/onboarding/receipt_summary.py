"""Summarize synthetic receipt rows by category using the Python standard library."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def summarize(source: Path) -> dict:
    totals: dict[str, Decimal] = {}
    count = 0
    with source.open(encoding='utf-8-sig', newline='') as stream:
        rows = csv.DictReader(stream)
        required = {'date', 'category', 'amount'}
        if not required.issubset(rows.fieldnames or []):
            raise ValueError('CSV requires date, category, amount columns')
        for number, row in enumerate(rows, start=2):
            category = (row.get('category') or '').strip()
            if not category:
                raise ValueError(f'Row {number}: category is empty')
            try:
                amount = Decimal(row.get('amount') or '')
            except InvalidOperation as exc:
                raise ValueError(f'Row {number}: amount is not a number') from exc
            if not amount.is_finite() or amount < 0:
                raise ValueError(f'Row {number}: amount must be finite and non-negative')
            totals[category] = totals.get(category, Decimal('0')) + amount
            count += 1
    return {'rows': count, 'totals': {key: str(value) for key, value in sorted(totals.items())}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    result = summarize(args.source)
    with args.output.open('w' if args.overwrite else 'x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
