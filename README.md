<h3 align="center">
	<img src="http://f52.tech/_nuxt/img/logo.89beae5.png" width="50" />
</h3>
<h4><p align="center">
A repository by F52 Technologies / Un dépôt par F52 Technologies.
</p></h4>
<p align="center">
contact: <a href="mailto:cedric@f52.tech">cedric@f52.tech</a>
</p>

# git-book-v2-examples-generator

Python script to generate Git Branching examples exactly as they are described in the git book (v2)

When you learn git, sometimes you read the [book](https://git-scm.com/book/en/v2) (or parts of it).

When you read the book about branching, sometimes you want to play with the example that is given.

Here is a Python script to generate those repositories, exactly as they appear in the git book, to play with as often as you'd like. For your own exercise, or for teaching.

You can either:
- `git clone` this repo, then run the script yourself: `python3 ./generator.py`
- run the following command to do the same immediately (it will create a directory named `git-book-v2-examples`, with examples repositories inside):
```bash
/usr/bin/env python3 -c "$(curl -fsSkL https://raw.githubusercontent.com/F52/git-book-v2-examples-generator/master/generator.py)"
```
- `git clone` the individual examples provided in the corresponding repositories.
