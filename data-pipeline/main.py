from logger import Logger
from dotenv import load_dotenv
import argparse

from common.dates import Date, DateRange

from ingestion.ingest import ingest_dates

from scoring.score import score_dates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process data pipeline arguments")

    # Ingest group
    ingest_group = parser.add_argument_group("ingest arguments")
    ingest_group.add_argument(
        "--ingest", action="store_true", help="Enable ingest mode"
    )
    ingest_group.add_argument(
        "--ingest-start",
        type=str,
        help="Start date for ingest (required if --ingest is set). Specified in YYYY-MM-DD format",
    )
    ingest_group.add_argument(
        "--ingest-end",
        type=str,
        help="End date for ingest (required if --ingest is set). Specified in YYYY-MM-DD format",
    )
    ingest_group.add_argument(
        "--ingest-name-source",
        type=str,
        choices=["dump", "api"],
        default="dump",
        help="Source for page name data (default: dump)",
    )
    ingest_group.add_argument(
        "--ingest-view-source",
        type=str,
        choices=["dump", "api"],
        default="dump",
        help="Source for view data (default: dump)",
    )
    ingest_group.add_argument(
        "--ingest-edit-source",
        type=str,
        choices=["dump_monthly", "dump_daily", "api"],
        default="dump_monthly",
        help="Source for edit data (default: dump_monthly)",
    )
    ingest_group.add_argument(
        "--ingest-batch-size",
        type=int,
        default=30000,
        help="Batch size for ingest operations (default: 30000)",
    )
    ingest_group.add_argument(
        "--ingest-batch-wait",
        type=float,
        default=0.0,
        help="Wait time between ingest batches in seconds (default: 0.0)",
    )
    ingest_group.add_argument(
        "--delete-dump-files",
        action="store_true",
        help="Delete dump files after ingesting that day's data",
    )
    ingest_group.add_argument(
        "--recreate-intermediate-table",
        action="store_true",
        help="Recreate the table with the new INTERMEDIATE_TABLE_SCHEMA. Use this carefully",
    )

    # Score group
    score_group = parser.add_argument_group("score arguments")
    score_group.add_argument("--score", action="store_true", help="Enable score mode")
    score_group.add_argument(
        "--score-start",
        type=str,
        help="Start date for scoring (required if --score is set). Specified in YYYY-MM-DD format",
    )
    score_group.add_argument(
        "--score-end",
        type=str,
        help="End date for scoring (required if --score is set). Specified in YYYY-MM-DD format",
    )
    score_group.add_argument(
        "--recreate-final-tables",
        action="store_true",
        help="Recreate the final table with their schemas. Use this carefully",
    )
    score_group.add_argument(
        "--score-tables",
        type=str,
        nargs="+",
        help="List of tables to score. If not provided, all tables will be scored",
    )

    args = parser.parse_args()

    if not args.ingest and not args.score:
        parser.error("At least one of --ingest or --score must be set")

    # Validate ingest arguments
    if args.ingest:
        if not args.ingest_start:
            parser.error("--ingest-start is required when --ingest is set")

        try:
            Date.from_str(args.ingest_start)
        except ValueError:
            parser.error("--ingest-start is not a valid date")

        if not args.ingest_end:
            parser.error("--ingest-end is required when --ingest is set")

        try:
            Date.from_str(args.ingest_end)
        except ValueError:
            parser.error("--ingest-end is not a valid date")
    else:
        if args.ingest_start:
            parser.error("--ingest-start can only be used when --ingest is set")
        if args.ingest_end:
            parser.error("--ingest-end can only be used when --ingest is set")

    # Validate score arguments
    if args.score:
        if not args.score_start:
            parser.error("--score-start is required when --score is set")

        try:
            Date.from_str(args.score_start)
        except ValueError:
            parser.error("--score-start is not a valid date")

        if not args.score_end:
            parser.error("--score-end is required when --score is set")

        try:
            Date.from_str(args.score_end)
        except ValueError:
            parser.error("--score-end is not a valid date")
    else:
        if args.score_start:
            parser.error("--score-start can only be used when --score is set")
        if args.score_end:
            parser.error("--score-end can only be used when --score is set")
        if args.recreate_final_tables:
            parser.error("--recreate-final-tables can only be used when --score is set")
        if args.score_tables:
            parser.error("--score-tables can only be used when --score is set")

    return args


if __name__ == "__main__":
    logger = Logger("data-pipeline")
    load_dotenv(dotenv_path=".env")
    args = parse_args()

    ingest: bool = args.ingest
    if ingest:
        ingest_start: Date = Date.from_str(args.ingest_start)
        ingest_end: Date = Date.from_str(args.ingest_end)
        ingest_name_source: str = args.ingest_name_source
        ingest_view_source: str = args.ingest_view_source
        ingest_edit_source: str = args.ingest_edit_source
        ingest_batch_size: int = args.ingest_batch_size
        ingest_batch_wait: float = args.ingest_batch_wait
        delete_dump_files: bool = args.delete_dump_files
        recreate_intermediate_table: bool = args.recreate_intermediate_table

        date_range = DateRange(ingest_start, ingest_end)

        if recreate_intermediate_table:
            print(
                "Recreate intermediate table argument passed. Please type 'I am sure' to confirm the operation. ONLY DO THIS IF YOU WANT TO DELETE ALL EXISTING DATA:"
            )
            confirm = input()
            if confirm != "I am sure":
                print("Aborting operation")
                exit(1)

        ingest_dates(
            logger=logger,
            date_range=date_range,
            name_source_str=ingest_name_source,
            view_source_str=ingest_view_source,
            edit_source_str=ingest_edit_source,
            batch_size=ingest_batch_size,
            batch_wait=ingest_batch_wait,
            delete_dump_files=delete_dump_files,
            recreate_table=recreate_intermediate_table,
        )

    score: bool = args.score
    if score:
        score_start: Date = Date.from_str(args.score_start)
        score_end: Date = Date.from_str(args.score_end)
        recreate_final_tables: bool = args.recreate_final_tables
        score_tables: list[str] = args.score_tables

        if recreate_final_tables:
            print(
                "Recreate final table argument passed . Please type 'I am sure' to confirm the operation. ONLY DO THIS IF YOU WANT TO DELETE ALL EXISTING DATA:"
            )
            confirm = input()
            if confirm != "I am sure":
                print("Aborting operation")
                exit(1)

        date_range = DateRange(score_start, score_end)
        score_dates(
            logger=logger,
            date_range=date_range,
            recreate_final_tables=recreate_final_tables,
            score_tables=score_tables,
        )
