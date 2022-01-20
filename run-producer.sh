topic=("bitcoin-topic" "ethereum-topic" "binance-topic" "tether-topic" "solana-topic")
word=("bitcoin" "ethereum" "binance" "tether" "solana")
for ((i = 0; i < 5; i++))
do
    python producer.py --topic=${topic[$i]} --word=${word[$i]} &
done