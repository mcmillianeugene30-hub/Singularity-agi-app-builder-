# Procfile for Heroku or other PaaS platforms
# Production web process

web: gunicorn api:app --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
