#!/bin/bash
# By LB
# run ETEX simulations
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
MM='NESTED TEST'
SUMMARY=""

warning() {
    printf "%-68s[$YELLOW%10s$NC]\n" "$@" "SKIPPED"
    return 0
}

report() {
    if [ $? -eq 0 ]; then
        printf "%-68s[$GREEN%10s$NC]\n" "$@" "OK"
        return 0
    else
        printf "%-68s[$RED%10s$NC]\n" "$@" "FAILED"
        return 1
    fi
}
summary() {
    if [ $? -eq 0 ]; then
        printf "%-68s[$GREEN%10s$NC]\n" "$@" "OK"
        SUMMARY+="$1: OK\n"
        return 0
    else
        printf "%-68s[$RED%10s$NC]\n" "$run_nests_test@" "FAILED"
        SUMMARY+="$1: FAILED\n"
        return 1
    fi
}
# Report the current working directory and the script's location
warning "[$MM] $PWD"
cd $(dirname $0)
# Check for Flexpart executable build before
test -f ../src/FLEXPART
report "[$MM] executable: ../src/FLEXPART" || exit 1
ln -s ../src/FLEXPART .
ln -s ../src/FLEXPART_ETA .
test -d ./default_options
report "[$MM] default options: ./default_options" || exit 1
cp -rf ./default_options ./current
if [ -d ./output ]; then
    rm -rf ./output/*
fi
mkdir -p ./output/
# Test counters
STATUS=0
TESTSRUN=0
#
###############################################################################
# BEGIN
sed -i "/LOUTNETCDFOUT=/c\ LOUTNETCDFOUT=  1," ./current/COMMAND

mkdir -p ./output/
./FLEXPART pathnames_nests
summary "[$MM] TEST METER $TESTSRUN (NESTS)"
STATUS=$((STATUS + $?))
TESTSRUN=$((TESTSRUN + 1))

./FLEXPART_ETA pathnames_nests
summary "[$MM] TEST ETA $TESTSRUN (ETA NESTS)"
STATUS=$((STATUS + $?))
TESTSRUN=$((TESTSRUN + 1))
#
# FINAL
#
echo -e "\n[$MM] SUMMARY:\n$SUMMARY"
echo "[$MM] Tests failed: $STATUS / $TESTSRUN"
#
# Return collective error status
#
exit $STATUS