import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class XSSScanner:
    """ Scanner de vulnérabilités XSS pour les sites web """
    
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            '"><img src=x onerror=alert(1)>',
            "<svg/onload=alert('XSS')>"
        ]

    def get_forms(self):
        """ Récupère tous les formulaires d'une page web """
        try:
            response = requests.get(self.target_url, timeout=5)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.find_all("form")
        except requests.RequestException as e:
            print(f"Erreur {e}")
            return []

    def get_form_details(self, form):

        details = {}
        details["action"] = form.attrs.get("action", "")
        details["method"] = form.attrs.get("method", "get").lower()
        details["inputs"] = []

        for input_tag in form.find_all("input"):
            input_name = input_tag.attrs.get("name")
            input_type = input_tag.attrs.get("type", "text")
            input_value = input_tag.attrs.get("value", "")
            details["inputs"].append({"name": input_name, "type": input_type, "value": input_value})

        return details

    def test_xss(self):
        """ Teste les formulaires pour les vulnérabilités XSS """
        forms = self.get_forms()
        for form in forms:
            form_details = self.get_form_details(form)
            target_url = urljoin(self.target_url, form_details["action"])
            method = form_details["method"]

            for payload in self.xss_payloads:
                data = {}

                for input in form_details["inputs"]:
                    if input["type"] in ["text", "search"]:
                        data[input["name"]] = payload
                    else:
                        data[input["name"]] = input["value"]


                try:
                    if method == "post":
                        response = requests.post(target_url, data=data, timeout=5)
                    else:
                        response = requests.get(target_url, params=data, timeout=5)

                    if payload in response.text:
                        print(f"XSS  {target_url} avec le payload: {payload}")
                        self.vulnerabilities.append({"url": target_url, "payload": payload})
                        

                except requests.RequestException as e:
                    print(f"[ERROR] Impossible de tester {target_url}: {e}")

    def generate_report(self):
        """ Affiche le resultat du scan """
        print("\n================= RAPPORT XSS =================")
        if not self.vulnerabilities:
            print("Rien!")
        else:
            print(f"{len(self.vulnerabilities)} vulnérabilités")
            for vuln in self.vulnerabilities:
                print(f"{vuln['url']} - Payload : {vuln['payload']}")
        print("==============================================\n")

# if __name__ == "__main__":
#     target_website = "http://testphp.vulnweb.com/"
#     scanner = XSSScanner(target_website)
#     scanner.test_xss()
#     scanner.generate_report()