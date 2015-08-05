fswatch -o ./ | xargs -n1 -I{} ./reload_finger.sh
