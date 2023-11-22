avg=0
c=0.0
tests=$1
txt=''

mkdir -p exec_times

if [ "$2" == "true" ] 
then
    txt="partial=true"
fi

for ((j=1; j<=16; j++));
do
    input='input=instances/'$j'.txt'
    for ((i=1; i<=$tests; i++));
    do
        echo 'python3 main.py ' $input ' time=true ' $txt ' '
        res="$(python3 main.py $input time=true $txt 2>&1 > /dev/null)"
        c=$( bc <<<"$c + $res" )
    done
    if [ "$2" == "true" ] 
    then 
        printf $j';'$tests';'$c'\n' >> exec_times/res_partiel.csv
    else
        printf $j';'$tests';'$c'\n' >> exec_times/res_full.csv
    fi
done