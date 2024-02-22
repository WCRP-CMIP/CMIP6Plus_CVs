freebase() {
  TOPIC=$(git branch | grep '*' | cut -d ' ' -f2)
  NEWBASE="${1:-main}"
  PREVSHA1=$(git rev-parse HEAD)

  echo "Freebasing $TOPIC onto $NEWBASE, previous SHA-1 was $PREVSHA1"
  echo "---"

  git reset --hard "$NEWBASE"
  git merge --squash "$PREVSHA1"
  git commit
}
