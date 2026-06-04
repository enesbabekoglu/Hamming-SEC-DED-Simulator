#!/bin/bash
# Hamming Simülatörü — macOS çift tıkla başlatıcı

cd "$(dirname "$0")" || exit 1

# Finder'dan açılınca PATH kısıtlı olabilir (pyenv, Homebrew)
export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

if ! command -v python3 >/dev/null 2>&1; then
    osascript -e 'display alert "Python 3 bulunamadı" message "Terminalde: pip3 install -r requirements.txt ve python3 main.py" as critical'
    exit 1
fi

python3 main.py
status=$?

if [ $status -ne 0 ]; then
    echo ""
    echo "Program hata ile kapandı (kod: $status)."
    echo "Terminalden deneyin: cd \"$(pwd)\" && python3 main.py"
    read -r -p "Kapatmak için Enter..."
fi

exit $status
