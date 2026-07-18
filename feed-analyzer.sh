#!/bin/bash

# top 5 most active users

file="twitter_dataset.csv"

if [ ! -f "$file" ]; then
    echo "Error: $file not found"
    exit 1
fi

echo "Top 5 Most Active Users"
echo "-----------------------"

# Username = column 2
# grep keeps only normal rows (some tweets are split on many lines)
grep "^[0-9]\+," "$file" | cut -d"," -f2 | sort | uniq -c | sort -nr | head -5
