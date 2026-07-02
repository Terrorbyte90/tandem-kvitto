import argparse
import sys
from logic import calculate_split


def parse_args():
    parser = argparse.ArgumentParser(
        description="Beräkna delat belopp med dricks."
    )
    parser.add_argument(
        "amount",
        type=float,
        help="Totalbeloppet (t.ex. 1000)",
    )
    parser.add_argument(
        "people",
        type=int,
        help="Antal personer (t.ex. 4)",
    )
    parser.add_argument(
        "tip_percent",
        type=float,
        help="Dricksprocent (t.ex. 10)",
    )
    parser.add_argument(
        "--special-percent",
        type=float,
        default=None,
        help="Procentandel som en specifik person betalar av totalbeloppet (t.ex. 50)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        result = calculate_split(
            args.amount, args.people, args.tip_percent, args.special_percent
        )
    except ValueError as e:
        print(f"Fel: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Totalbelopp med dricks: {result['total_med_dricks']:.2f}")

    if args.special_percent is not None:
        print(
            f"Specialperson ({args.special_percent:.0f}%): "
            f"{result['special_person_share']:.2f}"
        )
        print(
            f"Övriga {args.people - 1} personer: "
            f"{result['others_share']:.2f} var"
        )
    else:
        print(f"Varje person betalar: {result['per_person']:.2f}")


if __name__ == "__main__":
    main()
