#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applicazione Web Flask per l'Analisi del Sentiment
Autore: Assistente AI
Descrizione: App web che permette agli utenti di inserire recensioni e 
             ottenere un'analisi del sentiment in tempo reale.
"""

from flask import Flask, render_template_string, request
import re

# Inizializzazione dell'applicazione Flask
app = Flask(__name__)

def analizza_sentiment(recensioni):
    """
    Analizza il sentiment di una lista di recensioni.
    
    Args:
        recensioni (list): Lista di stringhe contenenti le recensioni
        
    Returns:
        dict: Dizionario con conteggi {'positive': int, 'negative': int, 'neutre': int}
        
    Logica:
        - Positive: contiene almeno una parola positiva
        - Negative: contiene solo parole negative (nessuna positiva)  
        - Neutre: non contiene né parole positive né negative
    """
    # Definizione delle parole chiave (case-insensitive)
    parole_positive = {"buono", "ottimo", "fantastico"}
    parole_negative = {"cattivo", "pessimo", "terribile"}
    
    # Inizializzazione contatori
    conteggi = {"positive": 0, "negative": 0, "neutre": 0}
    
    for recensione in recensioni:
        # Controllo se la recensione è vuota o contiene solo spazi
        if not recensione.strip():
            continue
            
        # Conversione in lowercase e estrazione delle parole
        # Utilizzo regex per separare solo caratteri alfabetici
        parole_recensione = set(re.findall(r'\b[a-zàáâãäåæçèéêëìíîïñòóôõöøùúûüý]+\b', 
                                         recensione.lower()))
        
        # Verifica presenza parole positive e negative
        ha_positive = bool(parole_recensione.intersection(parole_positive))
        ha_negative = bool(parole_recensione.intersection(parole_negative))
        
        # Classificazione secondo le regole di precedenza
        if ha_positive:
            conteggi["positive"] += 1
        elif ha_negative:
            conteggi["negative"] += 1
        else:
            conteggi["neutre"] += 1
    
    return conteggi

# Template HTML incorporato nell'applicazione
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analizzatore di Sentiment</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #34495e;
        }
        
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 12px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            box-sizing: border-box;
        }
        
        textarea:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
        }
        
        .submit-btn {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
            display: block;
            margin: 0 auto;
        }
        
        .submit-btn:hover {
            background-color: #2980b9;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        
        .result-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #bdc3c7;
        }
        
        .result-item:last-child {
            border-bottom: none;
        }
        
        .result-label {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .result-value {
            font-size: 1.2em;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
        }
        
        .positive { background-color: #27ae60; }
        .negative { background-color: #e74c3c; }
        .neutral { background-color: #95a5a6; }
        
        .help-text {
            font-size: 0.9em;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 5px;
        }
        
        .example {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .example h3 {
            margin-top: 0;
            color: #856404;
        }
        
        .reviews-analyzed {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Analizzatore di Sentiment</h1>
        
        <form method="POST">
            <div class="form-group">
                <label for="recensioni">Inserisci le tue recensioni:</label>
                <textarea 
                    name="recensioni" 
                    id="recensioni" 
                    placeholder="Inserisci una recensione per riga, ad esempio:&#10;Prodotto ottimo!&#10;Servizio cattivo&#10;Esperienza fantastica"
                    required>{{ input_text if input_text else '' }}</textarea>
                <div class="help-text">
                    💡 Ogni riga sarà considerata una recensione separata. 
                    Le parole chiave riconosciute sono:<br>
                    <strong>Positive:</strong> buono, ottimo, fantastico<br>
                    <strong>Negative:</strong> cattivo, pessimo, terribile
                </div>
            </div>
            
            <button type="submit" class="submit-btn">📊 Analizza Sentiment</button>
        </form>
        
        {% if risultati %}
        <div class="results">
            <h2>📈 Risultati dell'Analisi</h2>
            
            <div class="result-item">
                <span class="result-label">😊 Recensioni Positive:</span>
                <span class="result-value positive">{{ risultati.positive }}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">😞 Recensioni Negative:</span>
                <span class="result-value negative">{{ risultati.negative }}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">😐 Recensioni Neutre:</span>
                <span class="result-value neutral">{{ risultati.neutre }}</span>
            </div>
            
            <div class="reviews-analyzed">
                <strong>Totale recensioni analizzate:</strong> 
                {{ risultati.positive + risultati.negative + risultati.neutre }}
            </div>
        </div>
        {% endif %}
        
        <div class="example">
            <h3>📝 Esempio d'uso:</h3>
            <p>Prova a copiare e incollare queste recensioni nell'area di testo:</p>
            <code>
                Prodotto ottimo!<br>
                Servizio cattivo<br>
                Esperienza fantastica<br>
                Qualcosa di indifferente
            </code>
            <p><small>Risultato atteso: 2 positive, 1 negativa, 1 neutra</small></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rotta principale dell'applicazione.
    
    GET: Mostra il form per inserire le recensioni
    POST: Elabora le recensioni e mostra i risultati
    """
    risultati = None
    input_text = ""
    
    if request.method == 'POST':
        # Recupero del testo inserito dall'utente
        testo_recensioni = request.form.get('recensioni', '').strip()
        input_text = testo_recensioni  # Per mantenere il testo nel form
        
        if testo_recensioni:
            # Divisione del testo in recensioni separate (una per riga)
            recensioni_lista = [
                recensione.strip() 
                for recensione in testo_recensioni.split('\n') 
                if recensione.strip()  # Ignora righe vuote
            ]
            
            # Chiamata alla funzione di analisi
            if recensioni_lista:
                risultati = analizza_sentiment(recensioni_lista)
    
    # Rendering del template con i risultati (se presenti)
    return render_template_string(
        HTML_TEMPLATE, 
        risultati=risultati, 
        input_text=input_text
    )

@app.route('/api/sentiment', methods=['POST'])
def api_sentiment():
    """
    Endpoint API per l'analisi del sentiment (opzionale).
    Permette chiamate programmatiche all'analizzatore.
    
    Esempio di utilizzo:
    POST /api/sentiment
    Content-Type: application/json
    {"recensioni": ["Ottimo prodotto", "Servizio cattivo"]}
    """
    try:
        from flask import jsonify
        data = request.get_json()
        
        if not data or 'recensioni' not in data:
            return jsonify({'error': 'Campo recensioni mancante'}), 400
            
        recensioni = data['recensioni']
        if not isinstance(recensioni, list):
            return jsonify({'error': 'recensioni deve essere una lista'}), 400
            
        risultati = analizza_sentiment(recensioni)
        return jsonify(risultati)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Avvio dell'Analizzatore di Sentiment...")
    print("📍 Apri il browser all'indirizzo: http://localhost:5000")
    print("⚡ Premi Ctrl+C per fermare il server")
    
    # Avvio dell'applicazione Flask
    # debug=True abilita il ricaricamento automatico durante lo sviluppo
    app.run(debug=True, host='localhost', port=5000)