import argparse
import os
import typing

import pandas


def get_args() -> typing.Tuple[str, str, str]:
    """Parses arguments
    :return: tuple containing the defined arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Full path to the input file", required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Full path to the output file, when empty the input file will be overwritten",
        required=False,
    )
    parser.add_argument(
        "-a",
        "--action",
        help="Either 'zeros' to invalidate zeros or 'agg' for temporal aggregation",
        choices=("zeros", "agg"),
        required=True,
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise OSError("Input file does not exist")

    if not args.output:
        args.output = args.input

    return args.input, args.output, args.action


def invalidate_zeros(file_in: str, file_out: str):
    """Read file_in as csv, replaces zero's by None, writes the output to file_out
    :param file_in: input .csv file, expects columns: time (yyyy-mm-dd hh:mm:ss) and telemetry value
    :param file_out: output .csv file
    """
    telemetry_df = pandas.read_csv(file_in, names=["time", "telemetry"])
    telemetry_df["telemetry"].replace(to_replace=0, value=None, inplace=True)

    telemetry_df.to_csv(file_out, header=False, index=False)


def aggregate_telemetry(file_in: str, file_out: str):
    """Read file_in as csv, aggregates telemetry per hour, save result to the output file
    :param file_in: input .csv file, expects columns: time (yyyy-mm-dd hh:mm:ss) and telemetry value
    :param file_out: output .csv file
    """
    telemetry_df = pandas.read_csv(file_in, names=["time", "telemetry"])

    # convert time column to datetime, truncate to hours
    telemetry_df["hours"] = pandas.to_datetime(
        telemetry_df["time"], format="%Y-%m-%d %H"
    )

    # aggregate on the datetime column
    telemetry_df.set_index("hours", drop=False, inplace=True)
    telemetry_agg = telemetry_df.resample("H").sum()
    telemetry_agg.to_csv(file_out, header=False, index=True)


if __name__ == "__main__":
    file_in, file_out, action = get_args()

    if action == "zeros":
        invalidate_zeros(file_in, file_out)
    elif action == "agg":
        aggregate_telemetry(file_in, file_out)
