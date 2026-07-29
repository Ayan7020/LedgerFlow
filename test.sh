curl -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer RXf1q8kpyQtJKwgFtYCbFvJP' \
  -d '{"dt":"'"$(date -u +'%Y-%m-%d %T UTC')"'","message":"Hello from Better Stack!"}' \
  --insecure \
  https://s2636503.eu-central-1a.betterstackdata.com
