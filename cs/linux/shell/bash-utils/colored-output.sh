RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)
BOLD=$(tput bold)

info() {
    echo "$@"
}

success() {
    echo "${BOLD}${GREEN}$@${RESET}"
}

warning() {
    echo "${BOLD}${YELLOW}$@${RESET}"
}

error() {
    echo "${BOLD}${RED}$@${RESET}"
}
