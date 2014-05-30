#!/bin/sh
do_start () {
    eweestats.py
}
do_stop () {
    start-stop-daemon --stop --quiet
}
case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        exit $?
        ;;
    restart)
        do_stop
        sleep 1s
        do_start
        ;;
    reload|force-reload)
        echo "Error: argument '$1' not supported" >&2
        exit 3
        ;;
    *)
        echo "Usage: $0 start|stop|restart" >&2
        exit 3
        ;;
esac
exit 0
