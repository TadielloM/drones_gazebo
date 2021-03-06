#!/bin/bash
number=(5 10 15 20 25 30 40 50)
algorithms=("ORCA" "BAPF" "EAPF")
tests=(1 2)
for i in "${tests[@]}"
do
    for j in "${algorithms[@]}"
    do
        for k in "${number[@]}"
        do
            python generate.py -n $k -a $j -t $i
            gzserver drones_$k.world >> /home/matteo/test_paper/collisions/collisions_${k}_${j}_${i}.txt &
            if [ $j == "BAPF" ]
            then
                sleep `echo "$k*$k*0.02*60" | bc -l`
            else
                sleep 900
            fi
            echo "I'm killing the process for the test: $i, algo: $j, drones: $k"
            kill -15 `pidof gzserver`
            echo "I've killed the process for test: $i, algo: $j, drones: $k"
        done
        sleep 10s
    done
done

for j in "${algorithms[@]}"
do
    for k in "${number[@]}"
    do
        python generate.py -n $k -a $j -t 3
        gzserver drones_$k.world >> /home/matteo/test_paper/collisions/collisions_${k}_${j}_3.txt &
        sleep `echo "($k*2+5)*60" | bc -l`
        kill -15 `pidof gzserver`
        echo "I've killed the process for test: 3, algo: $j, drones: $k"
    done
    sleep 10s
done
