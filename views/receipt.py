from flask import Blueprint, request, render_template, redirect, url_for

from models import Session, Receipt

receipts_app = Blueprint('receipts_app', __name__)


@receipts_app.route('/', endpoint='index')
def index():
    return redirect(url_for('app.index'))


@receipts_app.route('/<int:data>/', endpoint='receipt_info', methods=('GET', 'POST'))
def receipt_info(data=None):
    receipt = Session.query(Receipt).filter(Receipt.id == data).one_or_none()

    if not receipt:
        return redirect(url_for("app.index"))

    return render_template("receipts/receipt.html", receipt=receipt)
