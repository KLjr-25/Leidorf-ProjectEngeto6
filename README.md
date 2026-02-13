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
- **Robustnost:** Implementováno ošetření dynamických prvků a srozumitelné české chybové hlášky.

## Instalace

1. Vytvořte virtuální prostředí:
    python -m venv venv
    .\venv\Scripts\Activate.ps1

2. Nainstalujte závislosti:
    pip install -r requirements.txt

3. Nainstalujte prohlížeč Playwright:
    playwright install chromium

## Spuštění
Projekt lze spustit jako běžný Python skript, který automaticky vyvolá testovací framework:
    python main.py

## Struktura projektu
- main.py: Hlavní a jediný soubor obsahující veškerou testovací logiku a spouštěč.
- .env: Konfigurační soubor pro uložení globálních proměnných (BASE_URL).
- requirements.txt: Seznam knihoven potřebných pro běh projektu.
