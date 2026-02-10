import argparse

parser = argparse.ArgumentParser(
    description="Display and/or log OBD data from vehicle"
)

parser.add_argument(
    "--testing",
    action="store_true",
    help="Will be either True or False",
)