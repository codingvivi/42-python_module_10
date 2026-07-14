
root-dir := justfile_directory()

name := "python_module_10"


src-dir := root-dir / "src"
tools-dir := root-dir / "tools"
dist-dir := root-dir / "dist"
stage-dir := dist-dir / name + "_turnin"


help:
    @just -l


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# run the entry script for the given exercise number
[group('run')]
run ex:
    uv run python {{src-dir}}/ex{{ex}}/*.py

[group('run')]
run-all:
  for f in {{src-dir}}/ex*/*.py; do uv run python "$f"; printf '\n\n'; done

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# dist
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# package a release tarball tagged with the given version
[group('dist')]
publish tag msg:
    just dist {{tag}}
    just tag {{tag}} {{msg}}
    git push origin HEAD:refs/heads/main --tags
    gh release create {{tag}} {{dist-dir}}/{{name}}_turnin_{{tag}}.tar.gz


# checks then stage + tarball
[group('dist')]
dist tag="":
    just clean
    just checks-dist
    just stage
    tar -czf {{dist-dir}}/{{name}}_turnin_{{tag}}.tar.gz -C {{stage-dir}} .

# rsync turnin files
[group('dist')]
stage:
    mkdir -p {{stage-dir}}
    rsync -vhacP --filter=':- .gitignore' src/ {{stage-dir}}/


# create tag for latest commit
[group('dist')]
tag name msg:
    #!/usr/bin/env nu
    if (git tag -l {{name}}| is-empty) {git tag {{name}} -m "{{msg}}"}

# type-check + style
[group('dist')]
checks-dist:
    just test-mypy
    just test-lint
    @printf '\033[1;32m✓ all checks passed! Ready for submission\n\033[0m\n'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# test
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# run mypy across src/
[group('test')]
test-mypy:
    uv run mypy --check-untyped-defs {{src-dir}}

# run ruff across src/
[group('test')]
test-ruff *args:
    uv run ruff check {{src-dir}} {{args}}

# run flake8 across src/
[group('test')]
test-flake8 *args:
    uv run flake8 {{src-dir}} {{args}}

[group('test')]
test-lint:
    just test-ruff
    just test-flake8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# remove python caches
[group('clean')]
clean:
    find {{src-dir}} -type d -name '__pycache__' -exec rm -rf {} +
    find {{src-dir}} -type f -name '*.pyc' -delete
    rm -rf {{root-dir}}/.mypy_cache {{root-dir}}/.ruff_cache 

# clean + remove dist tree
[group('clean')]
fclean: clean
    rm -rf {{dist-dir}}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# tools
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# run the interactive test-data generator
[group('tools')]
gen-data *args:
    uv run python {{tools-dir}}/data_generator.py {{args}}

