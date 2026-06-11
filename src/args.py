import argparse

parser = argparse.ArgumentParser(
    description="Display and/or log OBD data from vehicle"
)

parser.add_argument(
    "--testing",
    action="store_true",
    help="Will be either True or False",
)

parser.add_argument(
    "--skip",
    action="store_true",
)

parser.add_argument(
    "--idle_rpm",
    type=int,
    default=700
)