from flask import (
    Blueprint, abort, current_app, redirect, render_template, url_for
)
from sqlalchemy import ScalarResult
from werkzeug.exceptions import HTTPException, NotFound, Unauthorized

from app.database.postgre.models import CryptoCurrency
from app.database.postgre.services import PostgreHandler
from app.security import authorization_required


main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200


@main.route("/profile")
@authorization_required("access", scrf_header_requied=False)
def profile() -> tuple[str, int]:
    return render_template("profile.html", title="Profile"), 200


@main.route("/securities/navigation")
def securities() -> tuple[str, int]:
    return render_template("securities.html", title="Securities"), 200


@main.route("/crypto/list")
def crypto_list() -> tuple[str, int]:
    return render_template("cryptoList.html", title="Cryptocurrency"), 200


@main.route("/crypto/<string:ticker>")
def currency(ticker: str) -> tuple[str, int]:
    row: ScalarResult[CryptoCurrency] | None = PostgreHandler.get(
        CryptoCurrency,
        ticker=ticker
    )
    if row is None:
        abort(404)
    return render_template("cryptocurrency.html", title=ticker), 200


@main.route("/about")
def about() -> tuple[str, int]:
    return render_template("about.html", title="About"), 200


@main.route("/news")
def news() -> tuple[str, int]:
    return render_template("news.html", title="News"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200


@main.app_errorhandler(Unauthorized)
def handle_unauthorized(e: Unauthorized) -> tuple[str, int]:
    return redirect(url_for("main.index"), code=303)


@main.errorhandler(HTTPException)
def handle_exception(e: HTTPException) -> tuple[dict[str, str], int]:
    current_app.logger.error(f"Unhandled HTTPException: {e}", exc_info=True)
    return {"error": "Something went wrong!"}, 500
