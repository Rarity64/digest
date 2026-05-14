#!/bin/sh
cd "$(dirname "$0")"
SERVER_ADMIN_KEY=$(
    grep '=' .env | grep -v '^#' | sed 's/[[:space:]]*=[[:space:]]*/=/' | {
        while IFS= read -r line; do
            eval "export $line"
        done
        echo "${SERVER_ADMIN_KEY}"
    }
)
{
    echo "[$(date '+%F %T')]"
    curl -sS -w '\nHTTP_CODE=%{http_code}\n' -G \
        --data-urlencode "key=${SERVER_ADMIN_KEY}" \
        --data-urlencode "action=email_everything_to_everyone" \
        -- "http://localhost:8000/do/"
    echo
} 2>&1 | tee -a curl.log
