Zde je návrh souboru `README.md` pro tvou aplikaci **Akční plán**, zaměřený na vývojáře, kteří ji chtějí pochopit, rozšířit nebo integrovat do Jarvika:

---

````markdown
# 🛠️ Akční plán – modul pro Jarvik AI

Tento modul slouží k automatizovanému vytváření a správě akčních plánů na základě volného textu. Textový vstup je analyzován, rozdělen na základní komponenty (traceabilita, problém, řešení apod.) a uložen do strukturované paměti. Modul využívá RAG (retrieval-augmented generation) pro práci s historickými záznamy a umožňuje uživateli interaktivně upravovat a exportovat plánované akce.

---

## 🧱 Architektura

### 1. Backend (Flask)
- **Endpoint**: `/action_plan`
- **Typ požadavku**: `POST`
- **Tělo**: 
  ```json
  {
    "text": "Volný popis problému...",
    "user": "jiri"
  }
````

* **Funkce**:

  * Rozdělení textu na složky (traceabilita, problém, řešení)
  * Vyhledání v paměti (pomocí RAG)
  * Zápis nebo aktualizace záznamu dle rozhodnutí uživatele

### 2. UI (HTML/JS)

* Nová stránka `static/action_plan.html`
* Obsahuje:

  * Textarea pro vstup
  * Tlačítko pro analýzu a zápis
  * Tabulku všech záznamů
  * Filtry pro každý sloupec
  * Export do `.xlsx`
  * Sekci pro API klíč

### 3. Paměť

* Ukládáno jako `memory/<user>/action_plan.jsonl`
* Každý řádek = jeden záznam:

  ```json
  {
    "id": "AP-001",
    "traceability": "...",
    "problem": "...",
    "cause": "...",
    "action": "...",
    "responsible": "Jirka",
    "date": "2025-07-17",
    "effectiveness": "",
    "closed": false
  }
  ```

### 4. RAG (retrieval engine)

* Načítá paměť a hledá podobnosti mezi novým vstupem a historií
* Pokud se podobný záznam najde:

  * Nabídne uživateli výběr, zda aktualizovat
  * Jinak vytvoří nový záznam

---

## 🔐 API & bezpečnost

* API klíč zadává uživatel pouze jednou do UI
* Klíč je uložen lokálně v `config/user_settings.json` (mimo paměť a veřejné logy)
* V UI je tlačítko **Reset API**, které umožní klíč změnit

---

## 🧠 Volitelná neuronová soustava (doporučeno)

* Klasifikátor pro třídu textů (traceabilita / problém / řešení / příčina / opatření)
* Může být postaven jako:

  * Zero-shot klasifikace (`instruct` modely)
  * Jemně doladěný embedder (např. BERT, MiniLM)
* Možná integrace do `classify.py`

---

## 📤 Export

* Tabulka podporuje export do `.xlsx` přes frontend
* Exportovaný soubor obsahuje:

  * ID, Traceabilitu, Popis problému, Příčinu, Opatření, Osobu, Datum, Uzavření, Účinnost

---

## 📁 Struktura projektu

```
/app/
├── main.py                # Flask backend (rozšířen o /action_plan)
├── rag_engine.py          # Vyhledávání v paměti
├── memory.py              # Zápis/čtení z paměti
├── classifier.py          # (volitelně) neuronová klasifikace částí
/static/
├── action_plan.html       # Webové UI
├── action_plan.js         # JS logika
/config/
├── user_settings.json     # API klíče a nastavení
/memory/
└── jiri/
    └── action_plan.jsonl  # Paměťový soubor uživatele
```

---

## 🧪 Testovací scénář

1. Spusť `main.py` (`Flask` server)
2. Otevři `/static/action_plan.html`
3. Vlož volný text popisující problém
4. Odešli → backend analyzuje a uloží záznam
5. Zobrazí se v tabulce
6. Zkus další vstup → pokud se podobá předchozímu, nabídne přiřazení

---

## 🔮 Plánovaná rozšíření

* Notifikace pro zodpovědnou osobu (např. e-mailem)
* Automatické číslování `AP-XYZ`
* Historie revizí záznamů
* Přílohy (PDF, obrázky, dokumentace k problému)

---

## 📜 Licence

Interní použití v rámci projektu **Jarvik AI**. Neurčeno pro veřejnou distribuci bez souhlasu autora.

```

---

Chceš, abych ti rovnou vytvořil základní strukturu složek a souborů (`main.py`, `action_plan.html`, `memory/`, atd.)? Nebo raději po částech?
```
