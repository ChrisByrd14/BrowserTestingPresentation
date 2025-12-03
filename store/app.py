from flask import Flask, redirect, render_template

from .data import *

app = Flask(__name__)

@app.route('/')
@app.route('/store')
def index():
    items = Product.select().where(Product.deleted >> None)
    return render_template('index.html', items=items)


@app.route('/item/<slug>')
def item(slug: str):
    product = Product.get(Product.slug == slug)
    if not product:
        raise NotImplementedError()
    return render_template('item-details.html', item=product)


if __name__ == '__main__':
    app.run(port=8080)
