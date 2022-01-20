topic=("bitcoin-topic" "ethereum-topic" "binance-topic" "tether-topic" "solana-topic")

for ((i = 0; i < 5; i++))
do
    python consumer.py --topic=${topic[$i]} &
done