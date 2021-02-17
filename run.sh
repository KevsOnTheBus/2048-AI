#~\bin\bahs

# You will put your execution script here
# below is an example of a compiled and executed C++ program
# you may modify this script or delete it and start from scratch
# your bash script must be named "run.sh"

#g++ -std=c++11 *.cpp -o HelloAI
#./HelloAI

outFile="${1:0:-4}.out.txt"

python3 2048.py <$1 >$outFile
echo "Output printed in \"$outFile\""

