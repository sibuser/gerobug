#!/bin/bash

echo "[LOG] Waiting for dashboard to be ready"
sleep 15

echo "[LOG] GEROBUG-WEB is fully configured successfully."

exec "$@"
