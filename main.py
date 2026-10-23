import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(title="MINEPIA Vallée du Ntem - Système Complet de Collecte")

# --- CONNEXION CONFIGURATION STRICTE ---
{
  "type": "service_account",
  "project_id": "minepia-ntem-backend",
  "private_key_id": "ae0e2f1aacdeb577362e83907df3d9e5e05522e3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDlM6qLUx+Cxllk\nmXWVLUNU0PCGL1RFUYzu4DYnbsd8zCMMfRN4bD1UtD68LlysBl2ftf12bTSRVrqE\n0dAlGVzP0qQ0sgJZAlWRX4TP2i/eYPZ6JVPnGezRK+vUFqKzJiCw4nt5JCNpnl3W\nZgaOZu4TH2fRSh1iQqyIaqSdyjA9iDUC4jaq25gvUcYK/9fHSOzoiqO+rTwR88CA\nel57KGVAVSA7Jx03nhEOxExkv5NgaBn+6c+EkJQcjokYpOEkQtIGTxK0y5nqgLm/\nkB7Y2o+jIXSLUa0gXmap3rrDtK7OE709+/gehcIf7FqbAirzdQ5PVGzlfEEkuNVH\nHYxYfdmtAgMBAAECggEAWKnL52mYXvZrzkau/a4sxbqt0LquVsJdSmrhiA+Ki/RL\n+qDHz2XPs9ymCBXHM6Siww2bpxxHoZFzRb4ETtWo2ZwaeWgDEHuerkXNErrMmbHY\npxeZhWS5/5CGAd1fwv2U19hE+2/HYywoELAXCS84GZ2kg4mwJDq2k27tjzyPvL0g\naAlDBu7PpNJH2fXb1ijOc3o52Uj9EwlTzgbtIJ5cBU3t/WdvCkVc8hEDzVmRy2T4\nfRUtwm0YmjiKQJMQF/fgDVnqj21imHfILo2TjsQwwkN7sa8ena37+mfhrol42jjQ\n38RGQ3P6lo8rDq3m3vSXWYr/2GxXJOObZQxnm7/o4QKBgQD9wKUnuN8iyWmq9HqO\nvAdNS6+0xYNQqpdwE6psvdEs6CLk13H0OzpoeriR8rRpIqxiQ8v2zc93XRHOCQLH\neRONbpUe4pe/j09inEk//lKfUMdc00WLa00sOI5P4VAyP7RwsIq3biDDFP8AiFhB\nAQ8i7uoUkJYUrLvRU6+dgf9LYwKBgQDnO1rqwLCy6u+m9ehY1jdRSofqfqswMJss\nucU/x7n4aJNMpK7QblQ8qJXOqFsl/YYJ8mU6ybWcT4LTNCyOC7hbFAfolCl+Cxz6\nAyXj0XxkQqMkBsgww+KE65R52Ff4roHDDf8Lx3nG9DWizIjmBS99NUD4aHytD+mf\n73kdXfi7rwKBgGYkAVa357mM8WfK+PozXY0ThipxxqXVxRdsExGqZmR5HHKY9lmk\n7aHYpCq7UztupYz4VUWHGpelcuFIZ0H7zo8DkCractK80OuUlTeZG5DdZyJKOJgi\nHPJL4ZztyOYxFmS162Bih/V+ohaIy11/G6SoHrkgagjwbrmXwfzYsvaZAoGBAOCI\nHFKT5YD27Ns9Me8BpBmFu9ESSvyyVhvqEAVM1eLG+TGVQEMYvydftIhFpqyPL9b8\nzxt0vqsX8jtQEGumKdAW9U78gAXqmKqU3/gGdTmOE4hqJX5k19KmRzjBwTqziUF0\nl9JCUpfEj0iUP+LL6j80tPAB1f7e0scA7KR9mYf1AoGAcyqUVeBrQ+LUZ0Bv4wdE\nLWHolmpL1Mf82H/snRqbirW4RJQwzzbuM/ur4J6F/LQfllZvQOdRPi8xiUIr1Tnz\nOoj6WSjjmMZNREtVrwn/qKyWve5N8DcnM3SKc1J+qM1ZPaheFbuDC3XDZQydIjFz\nU2GrfQC8Wj4K9V/6Cu0iFEE=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@minepia-ntem-backend.iam.gserviceaccount.com",
  "client_id": "104826540017880761081",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40minepia-ntem-backend.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

CONFIG_FIREBASE = {
  "type": "service_account",
  "project_id": "minepia-ntem-backend",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://google.com",
  "token_uri": "https://googleapis.com",
  "auth_provider_x509_cert_url": "https://googleapis.com",
  "client_x509_cert_url": "..."
}

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(CONFIG_FIREBASE)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Erreur d'initialisation Firebase : {str(e)}")

db = firestore.client()

class FormulairePeche(BaseModel):
    arrondissement: str
    localite_debarcadere: str
    poids_capture_kg: float
    especes_dominantes: str
    nom_collecteur: str

@app.post("/nouvelle-collecte")
def enregistrer_collecte(data: FormulairePeche):
    arrondissements_valides = ["Ambam", "Kye-ossi", "Ma'an", "Olamze"]
    if data.arrondissement not in arrondissements_valides:
        raise HTTPException(
            status_code=400, 
            detail=f"L'arrondissement '{data.arrondissement}' ne fait pas partie de la Vallée du Ntem."
        )
    
    try:
        # Enregistrement direct et permanent dans Firebase Firestore
        doc_ref = db.collection("collectes_peche").document()
        donnees_fiches = data.dict()
        donnees_fiches["id_document"] = doc_ref.id
        
        doc_ref.set(donnees_fiches)
        
        return {
            "status": "Succès (Firebase en ligne)",
            "message": f"Données enregistrées définitivement pour l'arrondissement de {data.arrondissement}",
            "id_document_firebase": doc_ref.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'écriture Firebase : {str(e)}")

@app.get("/afficher-collectes")
def lister_collectes():
    try:
        collectes_ref = db.collection("collectes_peche").stream()
        liste_totale = [doc.to_dict() for doc in collectes_ref]
        return {"total": len(liste_totale), "donnees": liste_totale}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Firebase : {str(e)}")
