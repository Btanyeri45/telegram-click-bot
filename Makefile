.SILENT: reset-session

setup:
	python -m pip install requirements.txt
	python -m pip install requirements-dev.txt

reset-session:
	rm session.session 2>/dev/null || true
	rm session.session-journal 2>/dev/null || true
	echo "\nSession reset ✔\n"

run-mypy:
	python -m mypy cli.py telegram_cb/

run-prospector:
	python -m prospector --messages-only

format: format-black format-isort

format-black:
	python -m black cli.py telegram_cb/

format-isort:
	python -m isort -rc cli.py telegram_cb/
