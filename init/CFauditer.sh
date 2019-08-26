#!/bin/bash
# init script for Cloudflare audit log exporter

case "$1" in
  start)
        echo "Starting Cloudflare audit log exporter"
        /usr/bin/python /opt/CFauditer/CFauditer.py  &
        ;;
  stop)
        echo "Stopping Cloudflare audit log exporter"
        ps -ef | grep CFauditer.py | grep -v grep | awk '{print $2}' | head -n 1 | xargs kill -9
        ;;
  restart)
        ps -ef | grep CFauditer.py | grep -v grep | awk '{print $2}' | head -n 1 xargs kill -9
        sleep 2
        /usr/bin/python /opt/CFauditer/CFauditer.py &
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0
