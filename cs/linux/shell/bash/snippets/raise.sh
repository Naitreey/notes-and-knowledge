raise() {
    declare strerr=$1
    declare -a frame_infos
    declare -i frame=0
    declare frame_info
    while frame_info=$(caller $frame); do
        frame_infos[frame++]=$frame_info
    done
    ((frame=${#frame_infos[@]}-1))
    declare info
    echo "Traceback (most recent call last):"
    while [[ $frame -ge 0 ]]; do
        info=(${frame_infos[frame--]})
        printf '  File "%s", line %s, in %s\n' "${info[2]}" "${info[0]}" "${info[1]}"
    done
    echo "Exception: $strerr"
    exit 1
}
