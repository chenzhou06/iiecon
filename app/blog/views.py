from flask import render_template
from . import blog
from .. import flatpages

articles = flatpages


@blog.route("/")
def index():

    return render_template("blog/index.html", articles=articles)


@blog.route('/<path:path>/')
def article(path):
    article = articles.get_or_404(path)
    return render_template('blog/article.html', article=article)


@blog.route("/tag/<string:tag>/")
def tag(tag):
    tagged = [p for p in articles if tag in p.meta.get("tags", [])]
    return render_template("blog/tag.html", articles=tagged, tag=tag)
