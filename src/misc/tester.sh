avg=0
c=0.0
tests=$1

for ((j=1; j<=10; j++));
do
    input='input=instances/'$j'.txt'
    for ((i=1; i<=$tests; i++));
    do
        #echo $input
        res="$(python3 main.py $input time=true 2>&1 > /dev/null)"
        c=$( bc <<<"$c + $res" )
    done

    printf $j';'$tests';'$c'\n' >> res.csv
done