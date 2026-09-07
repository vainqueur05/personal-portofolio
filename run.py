import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, g, make_response, redirect, render_template, request, session, url_for

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY must be set in the environment")

app.config.update(
    LANGUAGES={"fr": "Français", "en": "English"},
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV", "production") == "production",
    SESSION_COOKIE_SAMESITE="Lax",
    TEMPLATES_AUTO_RELOAD=False,
)


def get_translation(lang):
    translation_file = BASE_DIR / "translations" / f"{lang}.json"
    fallback_file = BASE_DIR / "translations" / "fr.json"
    try:
        with translation_file.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with fallback_file.open("r", encoding="utf-8") as file:
            return json.load(file)


@app.before_request
def before_request():
    lang = request.args.get("lang")
    if lang in app.config["LANGUAGES"]:
        session["lang"] = lang
    if session.get("lang") not in app.config["LANGUAGES"]:
        cookie_lang = request.cookies.get("lang")
        session["lang"] = cookie_lang if cookie_lang in app.config["LANGUAGES"] else "fr"
    g.translations = get_translation(session["lang"])
    g.current_lang = session["lang"]


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = ("default-src 'self'; base-uri 'self'; "
        "form-action 'self' https://formspree.io; frame-ancestors 'self'; "
        "img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; script-src 'self'; connect-src 'self'")
    if request.is_secure:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.route("/set-language/<lang>")
def set_language(lang):
    if lang not in app.config["LANGUAGES"]:
        abort(404)
    session["lang"] = lang
    response = make_response(redirect(url_for("index")))
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 30,
                        secure=request.is_secure, httponly=True, samesite="Lax")
    return response


about_data = {
    "nom": "Vainqueur Kalema",
    "titre": "Développeur Web junior & Passionné de création numérique",
    "bio": [
        "Je suis développeur passionné par la création d'applications web modernes et performantes. J'ai commencé à coder il y a 2 années et depuis, je n'ai jamais cessé d'apprendre et d'explorer de nouvelles technologies.",
        "Titulaire d'un diplôme de licence en génie logiciel, j'ai travaillé sur divers projets universitaires allant du site vitrine à l'application web complexe. Ma philosophie : allier esthétique, fonctionnalité et expérience utilisateur.",
        "En dehors du code, je suis détenteur d'un diplôme d'état en électricité industrielle, passionné par la recherche, la lecture et les technologies financières, ce qui m'inspire souvent dans ma façon de résoudre les problèmes de manière créative.",
    ],
    "localisation": "Lubumbashi, République démocratique du Congo",
    "email": "vaiinqueurkalema035@gmail.com",
    "disponible": True,
}

services_data = [
    {"titre": "Site vitrine", "description": "Un site élégant et responsive pour présenter votre activité, vos produits ou vos services.", "icone": "bi-briefcase", "prix": "Sur devis", "features": ["Design sur mesure", "Optimisé mobile", "Formulaire de contact", "SEO de base"]},
    {"titre": "Portfolio professionnel", "description": "Mettez en valeur vos réalisations avec un portfolio moderne et épuré.", "icone": "bi-images", "prix": "Sur devis", "features": ["Galerie d'images", "Filtres par catégorie", "Page de détail", "Animations"]},
    {"titre": "Application web sur mesure", "description": "Développement d'applications web personnalisées avec Flask et JavaScript, de l'idée au déploiement.", "icone": "bi-gear", "prix": "Sur devis", "features": ["Backend Python/Flask", "Base de données", "Authentification", "API REST"]},
    {"titre": "Refonte de site", "description": "Modernisation d'un site existant pour améliorer son expérience, son design et ses performances.", "icone": "bi-arrow-repeat", "prix": "Sur devis", "features": ["Audit", "Nouveau design", "Performances", "Migration"]},
    {"titre": "Conseil & Formation", "description": "Conseils techniques et sessions adaptées à votre projet ou à votre progression en développement.", "icone": "bi-chat-dots", "prix": "Sur devis", "features": ["Analyse des besoins", "Recommandations techniques", "Cours particuliers", "Support"]},
]

competences_data = {
    "langages": [{"nom": "Python", "niveau": 60, "icone": "bi-filetype-py"}, {"nom": "JavaScript", "niveau": 25, "icone": "bi-filetype-js"}, {"nom": "HTML/CSS", "niveau": 55, "icone": "bi-filetype-html"}, {"nom": "SQL", "niveau": 45, "icone": "bi-database"}],
    "frameworks": [{"nom": "Flask", "niveau": 55, "icone": "bi-flask"}, {"nom": "Bootstrap", "niveau": 40, "icone": "bi-bootstrap"}],
    "outils": [{"nom": "Git", "niveau": 20, "icone": "bi-git"}, {"nom": "VS Code", "niveau": 95, "icone": "bi-code-square"}, {"nom": "Figma", "niveau": 65, "icone": "bi-pencil"}],
}


def load_projects():
    with (BASE_DIR / "data" / "projects.json").open("r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def index():
    return render_template("index.html", projects=load_projects())


@app.route("/about")
def about():
    return render_template("about.html", about=about_data)


@app.route("/competences")
def competences():
    return render_template("competences.html", competences=competences_data)


@app.route("/services")
def services():
    return render_template("services.html", services=services_data)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=load_projects())


@app.route("/project/<int:project_id>")
def project_detail(project_id):
    project = next((p for p in load_projects() if p["id"] == project_id), None)
    if project is None:
        abort(404)
    return render_template("projects_detail.html", project=project)


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="127.0.0.1", port=5000)
