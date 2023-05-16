#!/bin/bash
cd $(dirname $0)
cd /workspaces/ext-list
rm -rf /workspaces/ext-list/docs
/root/.pyenv/versions/3.8.16/bin/sphinx-build ./docs_src/ ./docs/
touch ./docs/.nojekyll
