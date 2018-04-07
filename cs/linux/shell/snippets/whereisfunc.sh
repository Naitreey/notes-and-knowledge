whereisfunc() {
    declare ret=0
    shopt -s extdebug
    declare -F "$1" || ret=1
    shopt -u extdebug
    return $ret
}
