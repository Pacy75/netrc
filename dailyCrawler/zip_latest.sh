#!/bin/bash
DATE=`date +%Y%m%d`
if [ -d "$DATE" ]; then
  zip -r "$DATE.zip" $DATE
fi
