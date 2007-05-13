#!/bin/bash

function running() {
	if [ -e "$pidfile" ] && kill -0 `cat "$pidfile"` > /dev/null 2>&1; then
		return 0
	else
		return 1
	fi
}

function terminate() {
	local pidfile=$1

	# Five tries to shut down nicely
	for i in `seq 5`; do
		if running; then
			echo "Still running..."
			kill `cat "$pidfile"`
			sleep 1
		else
			echo "Stopped running..."
			break;
		fi
	done

	# Time is up, bozo.
	if running; then
		echo "Killing..."
		kill -9 `cat "$pidfile"`
	fi
}

terminate /srv/t-names/Run/dns/twistd.pid
