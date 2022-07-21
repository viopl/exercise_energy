import argparse
import typing

import pandas

import src.tele_io as tele_io


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

    if not args.output:
        args.output = args.input

    return args.input, args.output, args.action


def read_telemetry(filename: str):
    """Reads the data from file and converts to pandas dataframe
    :param filename: csv file, expected columns: time (yyyy-mm-dd hh:mm:ss) and telemetry value
    :return: pandas dataframe
    """

    return pandas.read_csv(filename, names=["time", "telemetry"])


def invalidate_zeros(file_in: str, file_out: str):
    """Read file_in as csv, replaces zero's by None, writes the output to file_out
    :param file_in: input .csv file
    :param file_out: output .csv file
    """
    tele_io.check_file(file_in)
    tele_io.check_file_path(file_out)

    telemetry_df = read_telemetry(file_in)
    telemetry_df["telemetry"].replace(to_replace=0, value=None, inplace=True)

    telemetry_df.to_csv(file_out, header=False, index=False)


def aggregate_telemetry(file_in: str, file_out: str):
    """Read file_in as csv, aggregates telemetry per hour, save result to the output file
    :param file_in: input .csv file, expects columns: time (yyyy-mm-dd hh:mm:ss) and telemetry value
    :param file_out: output .csv file
    """
    tele_io.check_file(file_in)
    tele_io.check_file_path(file_out)

    telemetry_df = read_telemetry(file_in)

    # convert time column to datetime, truncate to hours
    telemetry_df["hours"] = pandas.to_datetime(
        telemetry_df["time"], format="%Y-%m-%d %H"
    )

    # aggregate on the datetime column
    telemetry_df.set_index("hours", drop=False, inplace=True)
    telemetry_agg = telemetry_df.groupby(telemetry_df.index.floor("H")).sum()
    # telemetry_df.resample("H").sum()  # it fills the gaps between missing hours
    telemetry_agg.to_csv(file_out, header=False, index=True)


if __name__ == "__main__":
    file_in, file_out, action = get_args()

    if action == "zeros":
        invalidate_zeros(file_in, file_out)
    elif action == "agg":
        aggregate_telemetry(file_in, file_out)
