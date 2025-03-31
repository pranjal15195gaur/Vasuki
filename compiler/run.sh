if [ -z "$1" ]; then
  python3 repl.py
fi

if [ ! -z "$1" ]; then
  python3 main.py $1
fi