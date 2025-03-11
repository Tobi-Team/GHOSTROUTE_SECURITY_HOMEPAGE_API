.PHONY: run mss-auto mms 

run-dev:
	@uvicorn app:app --reload --port=5000

test:
	@pytest

install:
	@pip install -r ./requirements.txt

mms-auto:
	@alembic revision --autogenerate -m $(msg)

mms:
	@alembic revision -m $(msg)

migrate:
	@alembic upgrade head

reverse-migrate:
	@alembic downgrade -1

celery:
	@celery -A api.celery worker --loglevel=info