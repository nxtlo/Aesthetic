# for auto-restart

while true; do
    python3.8 launcher.py
    for i in {5..1}; do
        echo “Restarting in $i”
        sleep 1
    done
done