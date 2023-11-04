#!/bin/bash

#cat "$1" | grep -v '/\*\*' | grep -v '\*/' | sed 's/ \*/#/g' | sed 's/ {/:/g' | sed 's/;//g' > tmp
cat "$1" | sed 's/this\./self\./g' > tmp
mv tmp "$1"

# end
