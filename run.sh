#!/bin/sh

# files to be run through maian, only run on combined contracts!
FILES=/app/input/contracts_combine/*.sol

cp -a /app/input/contracts_combine/. /MAIAN/tool/

ls /MAIAN/tool/

cd /MAIAN/tool

for filepath in $FILES
do
  # /app/input/MyContract.sol --> MyContract.sol
  filename=$(basename "$filepath")

  # ignore Migrations.sol file
  if [ $filename = "Migrations.sol" ]; then
    continue
  fi

  # MyContract.sol --> MyContract
  contractname=$(basename "$filepath" .sol)

  echo $filename
  echo $contractname

  python maian.py -s $filename $contractname -c 0 | tee /app/output/$filename
done
