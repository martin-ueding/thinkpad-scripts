#!/bin/bash
# Copyright © 2012 Jim Turner <jturner314@gmail.com>

case "$1" in
	resume|thaw)
		think-resume-hook
		;;
	suspend|hibernate)
		;;
	*)
		;;
esac
