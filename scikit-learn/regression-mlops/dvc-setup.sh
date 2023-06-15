git config --global user.email "ktos@example.com"
git config --global user.name "Jedrzej, Sebastian, Jakub"

git init
dvc init
git status

git add .dvc/config
git add .dvc/.gitignore
git add .dvcignore

git commit -m "feat: initialize dvc repo"

dvc add data/Aemf1.csv

git add data/.gitignore data/Aemf1.csv.dvc
git commit -m "feat: add Aemf1 dataset to dvc"

mkdir -p ~/dvcrepo
dvc remote add -d repozytorium ~/dvcrepo
git commit .dvc/config -m "feat: add local dir as remote dvc repo"

dvc push