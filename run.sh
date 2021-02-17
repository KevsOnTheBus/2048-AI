#~\bin\bahs


outFile="${1:0:-4}_sol.txt"

python3 2048.py <$1 #| tee $outFile
