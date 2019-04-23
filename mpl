#!/bin/bash

player=mplayer
#player=mpv
#player=vlc

#useOldMplayerOptions=1
useOldMplayerOptions=0


if [ $# -ne 0 ] && [  "$1" = "-3d" ]; then
	shift
	if [ $useOldMplayerOptions -ne 0 ] && [ "$player" = mplayer ]; then
		$player  -vo gl:stereo=3  --af=volnorm=1:1 "$@"
	else
		$player  -vo gl:stereo=3 "$@"
	fi
else
	if [ $useOldMplayerOptions -ne 0 ] && [ "$player" = mplayer ]; then
		$player --af=volnorm=1:1 "$@"
	else
		$player "$@"
	fi
fi
