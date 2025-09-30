#!/bin/bash

# bloco /22: 190.111.128.0 até 190.111.131.255
for i in {128..131}
do
  for j in {0..255}
  do
    ip="190.111.$i.$j"
    ptr=$(dig -x $ip +short)
    if [ -n "$ptr" ]; then
      echo "$ip -> $ptr"
    fi
  done
done
