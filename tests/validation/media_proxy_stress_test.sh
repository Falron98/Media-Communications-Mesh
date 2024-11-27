#!/bin/bash

NUM_TESTS=5

SENDER_DEVICE="0000:4b:11.3"
RECEIVER_DEVICE="0000:4b:11.4"
SENDER_PORT=9992
RECEIVER_PORT=9991

SENDER_IP="192.168.96.1"
RECEIVER_IP="192.168.96.2"

INPUT_FILE="input.yuv"
OUTPUT_FILE="output.yuv"

WIDTH=1920
HEIGHT=1080
FRAMERATE=30
PIXEL_FORMAT="yuv422p10le"

LOG_DIR="./logs"
mkdir -p $LOG_DIR

start_media_proxy() {
    local device=$1
    local port=$2
    sudo media_proxy -d $device -t $port &
    sleep 2
}

run_sender() {
    sudo MCM_MEDIA_PROXY_PORT=$SENDER_PORT ./sender_val
}

run_receiver() {
    sudo MCM_MEDIA_PROXY_PORT=$RECEIVER_PORT ./recver_val
}

cleanup() {
    echo "Interrupt received, cleaning up..."
    sudo pkill media_proxy
    exit 1
}

trap cleanup SIGINT

for ((i=1; i<=NUM_TESTS; i++))
do
    echo "Starting test iteration $i..."

    SENDER_LOG="$LOG_DIR/sender_log_$i.txt"
    RECEIVER_LOG="$LOG_DIR/receiver_log_$i.txt"

    start_media_proxy $SENDER_DEVICE $SENDER_PORT
    start_media_proxy $RECEIVER_DEVICE $RECEIVER_PORT

    sleep 2

    run_receiver > $RECEIVER_LOG 2>&1 &
    RECEIVER_PID=$!

    sleep 30

    kill -SIGINT $RECEIVER_PID

    sleep 5

    run_sender > $SENDER_LOG 2>&1 &
    SENDER_PID=$!

    sleep 30
    
    kill -SIGINT $SENDER_PID

    sleep 5

    echo "Test iteration $i completed."

    sudo pkill media_proxy
    sleep 2
done

echo "All tests completed."