# Progetto Django REST Weather Forecast API

## Descrizione

Questo progetto implementa un'API RESTful per fornire previsioni meteo basate su query utente (località, data, orario). Supporta due livelli di accesso:

- **Anonymous (pubblico):** fino a 10 richieste al giorno
- **Authenticated User:** richieste illimitate, con possibilità di salvare e visualizzare la cronologia delle query

Gli Authenticated User possono essere di due tipi:
- **user (normal user):** possono solo richiedere una previsione (non possono modificarle, aggiungerle, o eliminarle)
- **superuser (admin):** possono effettuare tutte le operazioni (GET, POST, PUT, PATCH, DELETE) disponibili.

Il progetto include anche un front-end minimale basato su template Django per testare gli endpoint API.

---

## Tecnologie usate
- Django REST Framework
- Autenticazione basata su sessione Django
- Front-end: HTML, CSS, JavaScript minimale

---

## Funzionalità principali

### API Endpoints

- `/api/forecast/`  
  Supporta GET, POST, PUT, PATCH, DELETE con gestione dinamica dell’ID risorsa (per PUT/PATCH/DELETE).  
  Permette ricerche con parametri: location, date, time.

- `/api/history/`  
  Visualizza la cronologia delle query effettuate dagli utenti registrati.
  Supporta GET e DELETE 

### Autenticazione

- Sistema di login/logout basato su sessione Django.
- Gestione CSRF token per richieste protette.
- Limitazione del numero di chiamate in base al gruppo (Anonymous vs Authenticated).

### Front-end

- Pagine HTML con form per testare i vari metodi HTTP e endpoint.
- Visualizzazione dinamica dei risultati in formato tabellare o JSON formattato.
- Campo dinamico per inserimento ID risorsa abilitato solo per PUT/PATCH/DELETE.
- Gestione del token CSRF e cookie di sessione in fetch API.
  
---

## 📦 Setup del progetto

1. **Clona il repository**

```bash
git clone https://github.com/iCecche/DjangoWeatherAPI.git
cd DjangoWeatherAPI
```

2. **Crea e attiva un virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # oppure .\venv\Scripts\activate su Windows
```

3. **Installa le dipendenze**

```bash
pip install -r requirements.txt
```

4. **Applica le migrazioni**

```bash
python manage.py migrate
```

5. **Preloaded Database (opzionale)**
```bash
python manage.py loaddata fixtures/initial_data.json
```
Usa il db con dati e utenti precaricati

6. **Crea un superuser (opzionale)**

```bash
python manage.py createsuperuser
```
> **NOTA:** per facilitare il testing è già stato creato un superuser 

7. **Avvia il server**

```bash
python manage.py runserver
```

---

## Endpoint disponibili

### 🔎 `GET /api/forecast/`

Restituisce una lista di previsioni. È possibile filtrare tramite query string:

```http
GET /api/forecast/?location=Roma&date=2025-06-27&time=12:00
```
Filtri disponibili: location, date, time

### ➕ `POST /api/forecast/`

Inserisce una o più previsioni. Accetta JSON con uno o più oggetti:

```json
[
  {
    "location": "Roma",
    "date": "2025-06-27",
    "time": "12:00",
    "temperature": 29,
    "description": "Soleggiato"
  },
  {
    "location": "Milano",
    "date": "2025-06-27",
    "time": "15:00",
    "temperature": 25,
    "description": "Pioggia leggera"
  }
]
```
I campi disponibili (e tutti required) sono: location, date, time, temperature e description

### 🛠️ `PUT /api/forecast/<id>/`

Aggiorna completamente un record esistente:

```json
{
  "location": "Roma",
  "date": "2025-06-28",
  "time": "18:00",
  "temperature": 27,
  "description": "Temporale"
}
```

### 🧩 `PATCH /api/forecast/<id>/`

Aggiorna parzialmente un record (es. solo temperatura):

```json
{
  "temperature": 30
}
```

### ❌ `DELETE /api/forecast/<id>/`

Elimina una previsione esistente.

---

## Endpoint aggiuntivi

### 🔎 `GET /api/history/`

Disponibile solo per utenti autenticati. Restituisce lo storico delle richieste effettuate.

---

## 🔐 Autenticazione

- Utenti anonimi: max 10 richieste al giorno.
- Utenti autenticati (premium): accesso illimitato + cronologia visibile.
- Autenticazione via form Django (`/api/login/`, `/api/logout/`, `/api/register/`).

### `POST /api/login/`
Effettua login sfruttando cookies sessions di Django

### `POST /api/register/`
Registra un nuovo utente tramite credenziali username + password

### `POST /api/logout/`
Effettua logout chiudendo la sessione 

Per facilitare il testing è già stato creato un utente user e superuser
- user → username: `user_test`, password: `customusertestpassword`
- superuser → username: `superuser_test`, password: `customsuperusertestpassword`

---

## Interfaccia di test (client minimale)

Visita la pagina `/api/home/` per accedere a un'interfaccia HTML semplice con:

- Selettore del metodo (GET, POST, PUT, PATCH, DELETE)
- Campo endpoint
- Campo payload JSON
- Campo ID (attivo solo per PUT/PATCH/DELETE)
- Pulsante per invio
- Risultato visualizzabile in modalità tabella o JSON

---

## 🌍 Deployment

L'app è online su Railway:

🔗 [https://djangoweatherapi-production.up.railway.app](https://djangoweatherapi-production.up.railway.app)
