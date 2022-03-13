all: build push
build:
	. _venv/bin/activate && \
	PATH=$$PATH:$$PWD python download.py
push:
	git add -A && \
	GIT_COMMITTER_NAME='Free Russia' GIT_COMMITTER_EMAIL='freerussia2022_1@protonmail.com' git commit --author="Free Russia <freerussia2022_1@protonmail.com>" --amend -m "some real news" && \
	git reflog expire --expire-unreachable=now --all && \
	git gc --prune=now && \
	git push -f origin main