import os
import json
from flask import Flask, render_template, request, flash, abort, redirect, url_for, session, g, make_response
from dotenv import load_dotenv

# chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)

# clé secrète
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

app.config['LANGUAGES'] = {'fr': 'Français', 'en': 'English'}
def get_translation(lang):
#"""Charge le fichier de traduction correspondant à la langue"""
    try:
        with open(f'APP/translations/{lang}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback vers français si fichier manquant
        with open('app/translations/fr.json', 'r', encoding='utf-8') as f:
            return json.load(f)

@app.before_request
def before_request():
#"""Avant chaque requête, on détermine la langue à utiliser"""
    # Priorité : paramètre 'lang' dans l'URL -> session -> cookie -> français
    lang = request.args.get('lang')
    if lang and lang in app.config['LANGUAGES']:
        session['lang'] = lang
    elif 'lang' not in session:
        # Récupérer depuis un cookie ou mettre français par défaut
        session['lang'] = request.cookies.get('lang', 'fr')

    # Stocker les traductions dans 'g' pour les rendre accessibles dans les templates
    g.translations = get_translation(session['lang'])
    g.current_lang = session['lang']

@app.route('/set-language/<lang>')
def set_language(lang):
#"""Route pour changer la langue (redirige vers la page précédente)"""
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang
        # Optionnel : stocker dans un cookie pour persister
        resp = make_response(redirect(request.referrer or url_for('index')))
        resp.set_cookie('lang', lang, max_age=60*60*24*30)  # 30 jours
        return resp
    return redirect(url_for('index'))
    

# Données personnelles pour la page "À propos"
about_data = {
'nom': 'Vainqueur Kalema',
'titre': 'Développeur Web junior & Passionné de création numérique',
'bio': [
"Je suis développeur passionné par la création d'applications web modernes et performantes. J'ai commencé à coder il y a 2 années et depuis, je n'ai jamais cessé d'apprendre et d'explorer de nouvelles technologies.",
"Titulaire d'un diplôme de licence en genie logiciel, j'ai travaillé sur divers projets universitaire allant du site vitrine à l'application web complexe. Ma philosophie : allier esthétique, fonctionnalité et expérience utilisateur.",
"En dehors du code, je suis detenteur d'un diplome d'état en électricité industriel, passionné par des recherches a plein temps,la lecture,les cryptomonaie(trading,bitcoin,.....),et bien d'autres, ce qui m'inspire souvent dans ma façon de résoudre les problèmes de manière créative."
    ],
'localisation': 'Lubumbashi, Republique Democratique du Congo',
'email': 'vaiinqueurkalema035@gmail.com',
'disponible': True  # True si disponible pour des missions
}

# Données personnelles pour la page "services"
services_data = [
    {
'titre': 'Site vitrine',
'description': 'Un site élégant et responsive pour présenter votre activité, vos produits ou vos services. Idéal pour les petites entreprises et les indépendants.',
'icone': 'bi-briefcase',
'prix': 'Sur devis',
'features': ['Design sur mesure', 'Optimisé mobile', 'Formulaire de contact', 'SEO de base']
    },
    {
'titre': 'Portfolio professionnel',
'description': 'Mettez en valeur vos réalisations avec un portfolio moderne et épuré. Parfait pour les photographes, artistes, développeurs, etc.',
'icone': 'bi-images',
'prix': 'Sur devis',
'features': ['Galerie d\'images', 'Filtres par catégorie', 'Page de détail', 'Animations']
    },
    {
'titre': 'Application web sur mesure',
'description': 'Développement d\'applications web personnalisées avec Flask et JavaScript. De l\'idée au déploiement, je vous accompagne.',
'icone': 'bi-gear',
'prix': 'Sur devis',
'features': ['Backend Python/Flask', 'Base de données', 'Authentification', 'API REST']
    },
    {
'titre': 'Refonte de site',
'description': 'Vous avez déjà un site mais il ne vous satisfait plus ? Je le modernise pour le rendre plus attractif et performant.',
'icone': 'bi-arrow-repeat',
'prix': 'Sur devis',
'features': ['Audit', 'Nouveau design', 'Amélioration des performances', 'Migration']
    },
    {
'titre': 'Conseil & Formation',
'description': 'Besoin de conseils sur votre projet web ? Ou envie d\'apprendre les bases du développement ? Je propose des sessions adaptées.',
'icone': 'bi-chat-dots',
'prix': 'Sur devis',
'features': ['Analyse des besoins', 'Recommandations techniques', 'Cours particuliers', 'Support']
    }
]

# Données personnelles pour la page "competences"
competences_data = {
'langages': [
        {'nom': 'Python', 'niveau': 60, 'icone': 'bi-filetype-py'},
        {'nom': 'JavaScript', 'niveau': 25, 'icone': 'bi-filetype-js'},
        {'nom': 'HTML/CSS', 'niveau': 55, 'icone': 'bi-filetype-html'},
        {'nom': 'SQL', 'niveau': 45, 'icone': 'bi-database'}
    ],
'frameworks': [
        {'nom': 'Flask', 'niveau': 55, 'icone': 'bi-flask'},
        {'nom': 'Bootstrap', 'niveau': 40, 'icone': 'bi-bootstrap'},
    ],
'outils': [
        {'nom': 'Git', 'niveau': 20, 'icone': 'bi-git'},
        {'nom': 'VS Code', 'niveau': 95, 'icone': 'bi-filetype-js'},
        {'nom': 'Figma', 'niveau': 65, 'icone': 'bi-pencil'},
    ]
}


#routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', about=about_data)


@app.route('/competences')
def competences():
    return render_template('competences.html', competences=competences_data)


@app.route('/services')
def services():
    return render_template('services.html', services=services_data)


def load_projects():
    with open('app/data/projects.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/projects')
def projects():
    projects_list = load_projects()
    return render_template('projects.html', projects=projects_list)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    projects_list = load_projects()

    project = next((p for p in projects_list if p['id'] == project_id), None)
    if project is None:
        abort(404)  # Page non trouvée
    return render_template('projects_detail.html', project=project)




@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)