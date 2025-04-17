import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="GrokAutoGen Investor CLI")
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = (
        parser.add_subparsers(dest="command", required=True)
    )

    # register
    register_parser: argparse.ArgumentParser = subparsers.add_parser(
        "register",
        help="Register a new user",
    )
    register_parser.add_argument(
        "--id",
        type=str,
        required=False,
        help="User id",
    )
    register_parser.add_argument(
        "--password",
        type=str,
        required=False,
        help="User password",
    )

    # login
    login_parser: argparse.ArgumentParser = subparsers.add_parser(
        "login",
        help="Login to the system",
    )
    login_parser.add_argument(
        "--id",
        type=str,
        required=False,
        help="User id",
    )

    # advice
    advice_parser: argparse.ArgumentParser = subparsers.add_parser(
        "advice",
        help="Get investment advice",
    )
    advice_parser.add_argument(
        "query",
        type=str,
        help="The query to ask",
    )

    # configure
    configure_parser: argparse.ArgumentParser = subparsers.add_parser(
        "configure",
        help="Configure settings",
    )
    configure_parser.add_argument(
        "--key",
        type=str,
        required=True,
        help="Configuration key",
    )
    configure_parser.add_argument(
        "--value",
        type=str,
        required=True,
        help="Configuration value",
    )

    args: argparse.Namespace = parser.parse_args()

    if args.command == "register":
        handle_register(args.id, args.password)
    elif args.command == "login":
        handle_login(args.id)
    elif args.command == "advice":
        handle_advice(args.query)
    elif args.command == "configure":
        handle_configure(args.key, args.value)


def handle_register(id: str = None, password: str = None) -> None:
    print(f"Handling 'register' command with id: {id}, password: {password}")


def handle_login(id: str = None) -> None:
    print(f"Handling 'login' command with id: {id}")


def handle_advice(query) -> None:
    print(f"Handling 'ask' command with query: {query}")


def handle_configure(key, value) -> None:
    print(f"Handling 'configure' command with key: {key}, value: {value}")


if __name__ == "__main__":
    main()
