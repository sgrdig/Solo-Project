# Importation des bibliothèques nécessaires
from src.xss import XSSScanner
import validators

"""Projets Scanner de Vulnérabilités Web
Objectif : Développer un scanner qui détecte les failles XSS, SQLi et CSRF"""

class VulnerabilityScanner(XSSScanner):
    def __init__(self, url):
        super().__init__(url)
        self.url = url


def isValidURL(url):
    """
    Vérifie si l'URL est valide.
    """
    if validators.url(url):
        return True
    else:
        return False


if __name__ =="__main__":
    print("Démarrage du scanner de vulnérabilités web...")

    url = None
    while not url or not isValidURL(url):
        url = input("Entrez l'URL à analyser : ")
        if not isValidURL(url):
            print("L'URL fournie n'est pas valide. Veuillez entrer une URL valide.")

    scanner = VulnerabilityScanner(url)
    scanner.test_xss()

    print("Analyse terminée.")