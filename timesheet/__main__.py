# Local imports
from timesheet import command_line_interface_functions as cli  # cli functions


def main():

    # Build interface
    parser = cli.build_command_line_interface()

    # Parse arguments
    cli.parse_command_line_arguments(parser)


if __name__ == "__main__":
    main()
