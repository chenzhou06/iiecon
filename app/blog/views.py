
from flask import render_template
from . import blog
from .. import flatpages


articles = flatpages


@blog.route("/")
def index():
    published = (p for p in articles if 'published' in p.meta)
    latest = sorted(published, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template("blog/index.html",
                           articles=latest[:10])


@blog.route('/<path:path>/')
def article(path):
    article = articles.get_or_404(path)
    return render_template('blog/article.html', article=article)


@blog.route("/tag/<string:tag>/")
def tag(tag):
    tagged = [p for p in articles if tag in p.meta.get("tags", [])]
    return render_template("blog/tag.html", articles=tagged, tag=tag)
