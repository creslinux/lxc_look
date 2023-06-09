rm static/*.html
venv/bin/pygmentize -f html -O style=monokai -O full -o static/first_version_1_be_src.html be.py
venv/bin/pygmentize -f html -O style=monokai -O full -o static/refactor_app_src.html be_app.py
venv/bin/pygmentize -f html -O style=monokai -O full -o static/refactor_platform_controller.html platform_controller/platform_controller.py
venv/bin/pygmentize -f html -O style=monokai -O full -o static/refactor_app_usecases_src.html platform_usecases/app_usecases.py
venv/bin/pygmentize -f html -O style=monokai -O full -o static/refactor_models_src.html platform_models/models.py
venv/bin/pygmentize -f html -O style=monokai -O full -o static/github_actions_pipeline.html .github/workflows/lxc-ec2.yml
