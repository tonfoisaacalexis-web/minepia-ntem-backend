import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(title="MINEPIA Vallée du Ntem - API Firebase Officielle")

# Emplacement de la clé privée téléchargée depuis Firebase
FICHIER_CLE = "firebase-key.json"

# Initialisation stricte de Firebase (sans mode local caché)
if not firebase_admin._apps:
    if os.path.exists(FICHIER_CLE):
        cred = credentials.Certificate(FICHIER_CLE)
        firebase_admin.initialize_app(cred)
    else:
        raise RuntimeError(
            f"ERREUR CRITIQUE : Le fichier '{FICHIER_CLE}' est introuvable dans votre dossier !"
        )

# Connexion directe à Firestore
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