# Projekt 6: Automatizované testy Playwright (Engeto)

Tento projekt obsahuje sadu tří automatizovaných testů pro webovou stránku Engeto.cz. Celý projekt je implementován v jediném souboru `main.py` s důrazem na profesionalitu, čistotu (PEP 8) a udržovatelnost pomocí architektury Page Object Model (POM).

## Funkce
- **Test 1:** Ověření správného načtení titulní stránky a titulku webu.
- **Test 2:** Ověření navigace do sekce Termíny a kontrola URL adresy.
- **Test 3:** Kontrola přítomnosti klíčového slova "Python" v aktuální nabídce kurzů.

## Technické standardy
- **Jednotný soubor:** Veškerá logika (POM, konfigurace, testy) je soustředěna v `main.py` pro snadné odevzdání.
- **Page Object Model (POM):** Logika selektorů je oddělena od samotných testovacích scénářů uvnitř třídy.
- **Zero Hardcoding:** URL a konfigurační data jsou načítána externě ze souboru `.env`.
- **Type Hinting:** Funkce a metody obsahují definice typů pro vyšší stabilitu kódu.
- **Robustnost:** Implementováno ošetření dynamických prvků (cookie banner, mobilní menu) a srozumitelné české chybové hlášky.

## Aktualizace a stabilizace (Reflexe technické revize)
Na základě zpětné vazby byla posílena stabilita a přesnost testů:
- **Error Handling:** Odstraněno tiché potlačování výjimek. Nyní jsou zachycovány specifické chyby (`PlaywrightTimeoutError`) a stavy jsou logovány do konzole.
- **Zpřesnění lokátorů:** Test 3 byl upraven tak, aby vyhledával klíčová slova pouze v hlavní obsahové části (`main`), čímž se předchází falešně pozitivním výsledkům z menu či patičky.
- **Anti-Flaky Navigace:** Posílena logika navigace s inteligentním ošetřením viditelnosti prvků (hamburger menu) a automatickým fallbackem na přímou URL.

## Instalace

1. **Vytvořte virtuální prostředí:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Nainstalujte závislosti:**
```powershell
pip install -r requirements.txt
```

3. **Nainstalujte prohlížeč Playwright:**
```powershell
playwright install chromium
```

## Spuštění

Projekt lze spustit dvěma způsoby:

1. **Automatické spuštění (včetně logování a UI):**
   ```powershell
   python main.py
   ```

2. **Manuální spuštění přes Pytest (pro detailnější výpis):**
   ```powershell
   pytest main.py -v -s --headed
   ```
   *Poznámka: Parametr `-s` je důležitý pro zobrazení logů o průběhu testu (cookies, navigace).*

## Struktura projektu
- **main.py:** Hlavní a jediný soubor obsahující veškerou testovací logiku a spouštěč.
- **.env:** Konfigurační soubor pro uložení globálních proměnných (BASE_URL).
- **requirements.txt:** Seznam knihoven potřebných pro běh projektu.
