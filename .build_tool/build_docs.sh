#!/bin/bash
cd $(dirname $0)
cd /workspaces/ext-list
/root/.pyenv/versions/3.8.16/bin/sphinx-build ./docs_src/ ./docs/
