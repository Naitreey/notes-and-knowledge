from colorama import Fore, Back


def echo(color, *lines):
    print(f"{color}%s{Fore.RESET}" % "\n".join(lines))


def info(*lines):
    echo(Fore.GREEN, *lines)


def warning(*lines):
    echo(Fore.YELLOW, *lines)


def error(*lines):
    echo(Fore.RED, *lines)

