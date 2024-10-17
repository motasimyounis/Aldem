sudo /home/ubuntu/Aldem/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/log/gunicorn/Aldempro.sock /home/ubuntu/Aldem/Aldempro.wsgi:application
