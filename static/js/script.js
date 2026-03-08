// script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('Le site est prêt !');

    // Fermer le menu mobile après clic sur un lien (pour les petits écrans)
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navLinks.length && navbarToggler && navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();  // simule un clic pour fermer
                }
            });
        });
    }

    // Ajouter une classe active à la page courante (optionnel)
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
