.ONESHELL:

# ------- Django Management Commands -------
check-migrations:
	python manage.py makemigrations --check --dry-run

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

create_test_users:
	python manage.py create_test_users

create_default_groups:
	python manage.py create_default_groups

# ------- Code Quality Commands -------
check-fix:
	black . && ruff check --fix-only --show-fixes --statistics .

show_envs:
	env | grep -E '^(ISHFLOW|DJANGO)'

# ------------- Server Run Commands -------------
run_server_local: collectstatic migrate create_test_users create_default_groups
	python manage.py runserver_plus 0.0.0.0:8000 --reloader-type=watchdog

run_server_prod:migrate collectstatic
	gunicorn --config src/settings/contrib/gunicorn.py src.wsgi:application

# ------------- Docker Compose Commands -------------
compose-up:
	docker compose -f docker/compose/local.yml up --build -d

compose-down:
	docker compose -f docker/compose/local.yml down

compose-reset-db:
	docker compose -f docker/compose/local.yml down -v
	docker compose -f docker/compose/local.yml up -d postgres-db
	sleep 5
	docker compose -f docker/compose/local.yml up --build -d

# ------------ Production Docker Compose Commands -------------
compose-prod-up:
	docker compose -f docker/compose/prod.yml up --build -d

compose-prod-down:
	docker compose -f docker/compose/prod.yml down

letsencrypt-cert:
	sh ./docker/scripts/init-letsencrypt.sh
