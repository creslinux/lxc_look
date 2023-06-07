rm static/*.html
pygmentize -f html -O style=monokai -O full -o static/first_version_1_be_src.html be.py
pygmentize -f html -O style=monokai -O full -o static/refactor_app_src.html be_app.py
pygmentize -f html -O style=monokai -O full -o static/refactor_platform_controller.html platform_controller/platform_controller.py
pygmentize -f html -O style=monokai -O full -o static/refactor_app_usecases_src.html platform_usecases/app_usecases.py
pygmentize -f html -O style=monokai -O full -o static/refactor_models_src.html platform_models/models.py
