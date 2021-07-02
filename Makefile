.SILENT: reset-session

reset-session:
	rm session.session 2>/dev/null || true
	rm session.session-journal 2>/dev/null || true
	echo "\nSession reset ✔\n"
