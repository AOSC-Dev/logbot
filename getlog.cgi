#!/bin/bash

IRC_LOG_FILE=irclog.log

if [ -n "$HTTP_IF_MODIFIED_SINCE" ]
then
    if [ "$(date -u -d "$HTTP_IF_MODIFIED_SINCE" +%s)" -ge "$(stat -c %Y "$IRC_LOG_FILE")" ]
    then
        echo 'Status: 304 Not Modified'
        echo
        exit 0
    fi
fi
echo 'Status: 200 OK'
echo 'Content-Type: text/html; charset=utf-8'
echo "Last-Modified: $(date -R -u -d @$(stat -c %Y $IRC_LOG_FILE))"
echo
if [ -n "$QUERY_STRING" ]
then
    line_count="$(tr -Cd [[:digit:]] <<< "$QUERY_STRING")"
else
    line_count=500
fi
if [ -n "$line_count" ]
then
    tail -n "$line_count" "$IRC_LOG_FILE" | fmtlog.py
else
    fmtlog.py < "$IRC_LOG_FILE"
fi

