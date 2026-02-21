import sys
from pathlib import Path
from colorama import init, Fore, Style
def main(match_id: str) -> None:
    None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ingest_match.py <match_id>")
    match_id = sys.argv[1]
    init(autoreset=True)
    print(
        f"{Fore.GREEN}{Style.BRIGHT}Starting ingestion for match ID: {match_id}{Style.RESET_ALL}"
    )
    main(match_id)
    print(
        f"{Fore.GREEN}{Style.BRIGHT}Finished ingestion for match ID: {match_id}{Style.RESET_ALL}"
    )
                                                                      


