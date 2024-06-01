attempts=0
max_attempts=5
while ! python manage.py check --database default; do
  if [ $attempts -eq $max_attempts ]; then
    echo "Max attempts reached, exiting"
    exit 1
  fi
  echo 'Waiting for the MySQL Server to be available...'
  sleep 5
  attempts=$((attempts+1))
done