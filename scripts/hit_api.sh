stocks_to_hit=("GOOG" "AMD")

if [[ -z $PORT ]]; then
  PORT=5000
fi

for stock in ${stocks_to_hit[@]}
  do
  echo "STOCK NAME: $stock"
  curl --silent "http://localhost:$PORT/stock/overview/$stock" | jq [.content]
  done