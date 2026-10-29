set -e
cd "$(dirname "$0")"
for s in hide_series allocation summary carbon crosscheck tables fig12 fig3 graphical_abstract; do python3 $s.py > /dev/null; echo "$s ok"; done
