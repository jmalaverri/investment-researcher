import argparse
import os
import sys

from dotenv import load_dotenv

from investment_researcher.adapters.alphavantage import AlphaVantageFundData
from investment_researcher.adapters.ollama import OllamaClient
from investment_researcher.errors import FundDataUnavailable, TickerNotFound
from investment_researcher.fundamentalist import Fundamentalist


def _print_report(report) -> None:
    print(f"Ticker: {report.ticker}")
    print(
        f"Expense ratio: {report.expense_ratio_pct:.2f}% ({report.expense_ratio_flag})"
    )
    print(f"Holdings count: {report.concentration.holdings_count}")
    print(f"Top 10 weight: {report.concentration.top_10_weight_pct:.2f}%")
    print(f"HHI: {report.concentration.hhi:.1f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fundamentalist v0 fund analyzer")
    parser.add_argument("ticker", help="Fund ticker symbol, e.g. VOO")
    parser.add_argument(
        "--interpret",
        action="store_true",
        help="Generate an LLM interpretation via Ollama",
    )
    args = parser.parse_args()

    load_dotenv()

    if not os.environ.get("FUND_API_KEY"):
        print("FUND_API_KEY is not set. Add it to your .env file and try again.")
        sys.exit(1)

    llm = OllamaClient() if args.interpret else None
    fundamentalist = Fundamentalist(AlphaVantageFundData.from_env(), llm=llm)

    if args.interpret:
        print("Generating interpretation (this may take ~30s)...", file=sys.stderr)

    try:
        report = fundamentalist.analyze(args.ticker.upper())
    except TickerNotFound:
        print(f"Ticker '{args.ticker.upper()}' was not found.")
        sys.exit(2)
    except FundDataUnavailable as exc:
        print(f"Fund data is currently unavailable: {exc}")
        sys.exit(3)

    _print_report(report)

    if report.interpretation is not None:
        print()
        print("Interpretation:")
        print(report.interpretation)
    elif args.interpret:
        print("Interpretation unavailable (LLM error).", file=sys.stderr)


if __name__ == "__main__":
    main()
