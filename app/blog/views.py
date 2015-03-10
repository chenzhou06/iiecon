from flask import render_template
from . import blog
from .. import flatpages

articles = flatpages


@blog.route("/")
def index():

    return render_template("blog/index.html", articles=articles)


@blog.route('/<path:path>')
def article(path):
    article = articles.get_or_404(path)
    return render_template('blog/article.html', article=article)
