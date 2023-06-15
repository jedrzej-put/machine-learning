for e in $(seq 10 10 60)
    do
        python src/train.py -d data/prepared -e $e 
    done