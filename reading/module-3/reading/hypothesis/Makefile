run: .venv
	. .venv/Scripts/activate; pytest

.venv:
	python -m venv .venv
	vim -E -s -c "source patch_venv.vimsrc" .venv/Scripts/activate  # Correct the path for Mys
	. .venv/Scripts/activate; pip install -r requirements.pip


