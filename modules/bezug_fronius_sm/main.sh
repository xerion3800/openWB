#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
    MYLOGFILE="$RAMDISKDIR/openWB.log"
else
    MYLOGFILE="$RAMDISKDIR/evu_json.log"
fi

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "bezug_fronius_sm: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

python3 /var/www/html/openWB/packages/modules/fronius/device.py "counter_sm" "${wrfroniusip}" "${froniuserzeugung}" "0" "${froniusvar2}" "0" "0" "none" "" &>>$MYLOGFILE
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
