# Programmering 2 – Gruppuppgift (Jordskälvsstatistik)

Flask-applikation för visning och analys av jordskälvsdata från USGS API.

## Projektarbete & Git Workflow

1. **Klona repot**

   ```bash
   git clone <repo-URL>
   cd <repo-mapp>
   ```

2. **Skapa och aktivera virtuell miljö**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS / Linux / WSL
    venv\Scripts\activate # Windows (CMD / PowerShell)
    ```

3. **Installera beroenden**

    ```bash
    pip install -r requirements.txt
    ```

4. **Skapa en egen branch**

    *Arbeta alltid i din egen branch, aldrig direkt i main!*

    ```bash
    git switch -c branch-namn
    ```

5. **Kontroller före commit**

    *Linta koden:
    ```Bash
    ruff check .
    ```
    
    *Formatera koden:
    ```Bash
    ruff format .
    ```

    *Kör tester:
    ```Bash
    pytest
    ```

6. **Starta applikationen:**

    ```bash
    flask run --debug
    ```
    Applikationen körs på: <http://127.0.0.1:5000/>

## Routar & Uppgifter

* `/` (HEM): Hemsida
* `/magnitude` (Route 1): Magnitud & djup (Oscar)
* `/map` (Route 2): Geografisk karta över jordbävningar (Gabriel)
* `/timeline` (Route 3): Tidslinje & trender (Eliska)



