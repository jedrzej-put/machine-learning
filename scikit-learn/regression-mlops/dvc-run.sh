dvc run --force -n prepare \
    -p prepare.seed,prepare.split \
    -d src/prepare.py -d data/Aemf1.csv \
    -o data/prepared \
    python src/prepare.py data/Aemf1.csv