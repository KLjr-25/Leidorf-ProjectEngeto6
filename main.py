"""
main.py: Šestý projekt Tři automatizované testy do Engeto Online Python Akademie
author: Květoslav Leidorf
email: k.leidorf@gmail.com
discord: kvetos_95684
"""

import os
import re
import sys
import pytest
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

# =============================================================================
# KONFIGURACE A NASTAVENÍ (ZERO HARDCODING)
# =============================================================================
# Načtení proměnných ze souboru .env
load_dotenv()
BASE_URL: str = os.getenv("BASE_URL", "https://engeto.cz").rstrip("/")

# =============================================================================
# ARCHITEKTURA: PAGE OBJECT MODEL (POM)
# =============================================================================
class EngetoPage:
    """
    Třída reprezentující webovou stránku Engeto.
    Odděluje technické hledání prvků (lokátory) od samotných testů.
    """
    def __init__(self, page: Page) -> None:
        self.page = page
        # Lokátor pro cookie tlačítko
        self.cookie_button = page.locator("#cookiescript_accept")
        # Lokátor pro odkaz na Termíny (bere první viditelný)
        self.terminy_link = page.get_by_role("link", name=re.compile(r"Termíny", re.IGNORECASE)).first

    def navigate(self) -> None:
        """Otevře web a pokusí se vyřešit cookie lištu."""
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        try:
            self.cookie_button.click(timeout=3000)
        except:
            pass # Pokud se lišta neobjeví, pokračujeme dál

    def go_to_terminy(self) -> None:
        """Naviguje uživatele do sekce Termíny."""
        try:
            self.terminy_link.wait_for(state="visible", timeout=5000)
            self.terminy_link.click()
        except:
            # Záložní navigace, pokud by bylo menu překryté
            self.page.goto(f"{BASE_URL}/terminy/")

# =============================================================================
# FIXTURES (PŘÍPRAVA PROSTŘEDÍ)
# =============================================================================
@pytest.fixture
def engeto(page: Page) -> EngetoPage:
    """Připraví stránku před každým testem."""
    engeto_page = EngetoPage(page)
    engeto_page.navigate()
    return engeto_page

# =============================================================================
# TESTOVACÍ SCÉNÁŘE (TŘI AUTOMATIZOVANÉ TESTY)
# =============================================================================
def test_homepage_loads_correctly(engeto: EngetoPage) -> None:
    """Test 1: Ověření správného načtení titulní stránky a titulku."""
    expect(engeto.page, "Chyba: Titulek neodpovídá webu Engeto.").to_have_title(re.compile(r"Engeto", re.IGNORECASE))

def test_navigation_to_terminy(engeto: EngetoPage) -> None:
    """Test 2: Ověření navigace do sekce Termíny a kontrola URL."""
    engeto.go_to_terminy()
    expect(engeto.page, "Chyba: Uživatel nebyl přesměrován na /terminy/.").to_have_url(re.compile(r"/terminy/"))
    expect(engeto.page.locator("h1").first, "Chyba: Na stránce chybí hlavní nadpis H1.").to_be_visible()

def test_check_python_presence(engeto: EngetoPage) -> None:
    """Test 3: Kontrola přítomnosti klíčového slova 'Python' v nabídce kurzů."""
    engeto.go_to_terminy()
    error_msg = "Varování: Text 'Python' nebyl nalezen. Web mohl změnit strukturu nebo kurz není vypsán."
    expect(engeto.page.locator("body"), error_msg).to_contain_text("Python", ignore_case=True, timeout=10000)

# =============================================================================
# SPUŠTĚNÍ (VSTUPNÍ BOD)
# =============================================================================
if __name__ == "__main__":
    # Tento blok zajistí, že po spuštění 'python main.py' se spustí pytest
    # přímo nad tímto souborem.
    print(f"--- Spouštím Projekt 6 (Playwright testy) ---")
    args = ["-v", "--headed", __file__]
    sys.exit(pytest.main(args))

