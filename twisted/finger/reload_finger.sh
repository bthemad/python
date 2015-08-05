clear
echo "killing all things"
killall python
echo "reloading"
python ./finger.py 2>&1 &
echo "=== ==="

