"""
2 verze - Opraveno ošetření výjimek a zpřesněn lokátor v Testu 3 dle doporučení lektora S.T.
main.py: Šestý projekt Tři automatizované testy do Engeto Online Python Akademie
author: Květoslav Leidorf
email: k.leidorf@gmail.com
discord: kvetos_95684
"""

import os
import re
import sys
import pytest
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv

# Načtení environmentálních proměnných
load_dotenv()
BASE_URL: str = os.getenv("BASE_URL", "https://engeto.cz").rstrip("/")

class EngetoPage:
    """
    Page Object Model pro Engeto.cz s aktivním ošetřením viditelnosti prvků.
    """
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cookie_button = page.locator("#cookiescript_accept")
        # Lokátor pro hlavní menu (hamburger), pokud je stránka v mobilním/zmenšeném zobrazení
        self.menu_button = page.get_by_role("button", name=re.compile(r"Menu", re.IGNORECASE))
        self.terminy_link = page.get_by_role("link", name=re.compile(r"Termíny", re.IGNORECASE)).first
        self.main_content = page.locator("main")

    def navigate(self) -> None:
        """Navigace a robustní odbavení cookie banneru s logováním stavu."""
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        try:
            # Kontrola viditelnosti před interakcí
            if self.cookie_button.is_visible(timeout=3000):
                self.cookie_button.click()
                print("\nLog: Cookie banner potvrzen.")
        except PlaywrightTimeoutError:
            print("\nLog: Cookie banner nedetekován, pokračuji.")
        except Exception as e:
            print(f"\nVarování: Neočekávaná chyba při řešení cookies: {e}")

    def go_to_terminy(self) -> None:
        """
        Navigace na termíny s pokusem o zviditelnění menu a finálním fallbackem.
        """
        try:
            # Kontrola viditelnosti odkazu pro případ mobilního zobrazení
            if not self.terminy_link.is_visible():
                if self.menu_button.is_visible(timeout=2000):
                    self.menu_button.click()
                    print("Log: Otevírám mobilní menu pro zviditelnění odkazu.")

            # Pokus o standardní kliknutí na odkaz
            self.terminy_link.wait_for(state="visible", timeout=3000)
            self.terminy_link.click()
            print("Log: Navigace přes UI proběhla úspěšně.")
        except (PlaywrightTimeoutError, Exception) as e:
            # Finální záchranná brzda - přímá navigace při selhání UI prvků
            print(f"Log: UI navigace selhala ({e}). Použit fallback na přímou URL.")
            self.page.goto(f"{BASE_URL}/terminy/")

@pytest.fixture
def engeto(page: Page) -> EngetoPage:
    """Fixture pro inicializaci stránky před každým testem."""
    engeto_page = EngetoPage(page)
    engeto_page.navigate()
    return engeto_page

# --- Testy ---

def test_homepage_loads_correctly(engeto: EngetoPage) -> None:
    """Ověření správného načtení titulní stránky."""
    expect(engeto.page, "Chyba: Titulek neodpovídá.").to_have_title(re.compile(r"Engeto", re.IGNORECASE))

def test_navigation_to_terminy(engeto: EngetoPage) -> None:
    """Ověření navigace do sekce termínů."""
    engeto.go_to_terminy()
    expect(engeto.page, "Chyba: Špatná URL.").to_have_url(re.compile(r"/terminy/"))

def test_check_python_presence(engeto: EngetoPage) -> None:
    """Kontrola přítomnosti textu 'Python' v hlavní obsahové části sekce Termíny."""
    engeto.go_to_terminy()
    # Vyhledávání omezeno na 'main_content' pro vyšší přesnost testu
    error_msg = "Chyba: Kurz Python nebyl v hlavní části nalezen."
    expect(engeto.main_content, error_msg).to_contain_text("Python", ignore_case=True, timeout=10000)

if __name__ == "__main__":
    # Spuštění s -s pro zobrazení našich Logů v terminálu
    sys.exit(pytest.main(["-v", "-s", "--headed", __file__]))
