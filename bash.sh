#!/bin/bash

# --- Variables ---
name="Hackerman"
count=3
readonly pi=3.14
declare -a colors=("red" "green" "blue")

# --- Functions ---
greet() {
    echo "Hello, $name!"
}

factorial() {
    local n=$1
    if (( n <= 1 )); then
        echo 1
    else
        echo $(( n * $(factorial $((n - 1)) ) ))
    fi
}

# --- Control Flow ---
for color in "${colors[@]}"; do
    echo "Color: $color"
done

if [[ $count -gt 2 ]]; then
    greet
else
    echo "Too few counts"
fi

# --- Command Substitution and Pipes ---
date_now=$(date "+%Y-%m-%d %H:%M:%S")
echo "Current date: $date_now"
ps aux | grep "$USER" | awk '{print $1, $2, $11}' | head -n 5

# --- Heredoc and Redirection ---
cat <<EOF > output.txt
This is a test.
Generated on: $date_now
EOF

# --- Arithmetic and Subshell ---
((count++))
echo "Factorial of $count: $(factorial $count)"