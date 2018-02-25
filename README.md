<h3 align="center">
	<img src="http://f52.tech/_nuxt/img/logo.89beae5.png" width="50" />
</h3>
<h4><p align="center">
A repository by F52 Technologies / Un dépôt par F52 Technologies.
</p></h4>
<p align="center">
contact: <a href="mailto:cedric@f52.tech">cedric@f52.tech</a> | website: <a href="http://f52.tech">http://f52.tech</a>
</p>

# git-book-v2-examples-generator [en]

When you learn git, sometimes you read the [book](https://git-scm.com/book/en/v2) (or parts of it).

When you read the book about branching, sometimes you want to play with the example that is given.

Here is a Python script to generate those repositories, exactly as they appear in the git book, to play with as often as you'd like. For your own exercise, or for teaching.

You can either:
- `git clone` this repo, then run the script yourself: `python3 ./generator.py`
- run the following command to do the same immediately (it will create the examples repositories where the command is executed):
```bash
/usr/bin/env python3 -c "$(curl -fsSkL https://raw.githubusercontent.com/F52/git-book-v2-examples-generator/master/generator.py)"
```
- `git clone` the individual examples provided in the corresponding repositories in [GitHub F52 account](https://github.com/F52).

# git-book-v2-examples-generator [fr]

Quand vous apprenez git, des fois, vous lisez le [livre](https://git-scm.com/book/fr/v2) (ou au moins des morceaux).

Et quand vous lisez le livre au chapitre des branches, des fois, voulez jouer avec les exemples qui sont donnés.

Ici se trouve donc un script Python3 pour générer ces dépôts git, exactement comme ils apparaissent dans le livre, pour vous permettre de jouer et expérimenter avec autant de fois que vous le désirez. Pour vos propres exercices, ou pour les enseigner.

Vous pouvez soit:
- exécuter `git clone` sur ce dépôt, et ensuite exécuter le script vous-même: `python3 ./generator.py`
- éxecuter la commande suivante qui va le faire automatiquement (les dépôts seront créés à l'endroit où la commande est lancée):
```bash
/usr/bin/env python3 -c "$(curl -fsSkL https://raw.githubusercontent.com/F52/git-book-v2-examples-generator/master/generator.py)"
```
- exécuter `git clone` sur les exemples individuels fournis dans les dépôts correspondants sur le [compte GitHub de F52](https://github.com/F52).
