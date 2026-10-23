import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(title="MINEPIA Vallée du Ntem - Système Complet de Collecte")

# --- CONNEXION CONFIGURATION SÉCURISÉE ET COMPATIBLE RENDER ---
# On récupère le dossier actuel où se trouve ce fichier main.py
DOSSIER_ACTUEL = os.path.dirname(os.path.abspath(__file__))
# On crée le chemin complet vers le fichier firebase-key.json
CHEMIN_CLE_FIREBASE = os.path.join(DOSSIER_ACTUEL, "firebase-key.json")

if not firebase_admin._apps:
    if os.path.exists(CHEMIN_CLE_FIREBASE):
        try:
            cred = credentials.Certificate(CHEMIN_CLE_FIREBASE)
            firebase_admin.initialize_app(cred)
            print("🚀 Firebase a été initialisé avec succès sur Render !")
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier de clé : {str(e)}")
    else:
        raise RuntimeError(
            f"ERREUR CRITIQUE : Le fichier de clé est introuvable au chemin : {CHEMIN_CLE_FIREBASE}"
        )

# Connexion directe au client de la base de données Firestore
db = firestore.client()

# --- MODÈLES DE REQUÊTES ---

class FormulairePeche(BaseModel):
    arrondissement: str
    localite_debarcadere: str
    poids_capture_kg: float
    especes_dominantes: str
    nom_collecteur: str

class FormulaireElevage(BaseModel):
    arrondissement: str
    localite_village: str
    type_cheptel: str
    nombre_tetes: int
    animaux_vaccines: int
    nom_collecteur: str

class FormulaireIndustrie(BaseModel):
    arrondissement: str
    type_infrastructure: str
    nom_etablissement: str
    volume_viande_kg: float
    infractions_constatees: str
    nom_inspecteur: str

# --- FONCTION DE VALIDATION COMMUNE ---
def valider_arrondissement(nom: str):
    arrondissements_valides = ["Ambam", "Kye-ossi", "Ma'an", "Olamze"]
    if nom not in arrondissements_valides:
        raise HTTPException(
            status_code=400, 
            detail=f"L'arrondissement '{nom}' ne fait pas partie de la Vallée du Ntem."
        )

# --- ROUTES DE SAISIES ---

@app.post("/collecte/peche")
def enregistrer_peche(data: FormulairePeche):
    valider_arrondissement(data.arrondissement)
    try:
        doc_ref = db.collection("collectes_peche").document()
        donnees = data.dict()
        donnees["id_document"] = doc_ref.id
        doc_ref.set(donnees)
        return {"status": "Succès (Firebase)", "message": "Fiche Pêche enregistrée", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collecte/elevage")
def enregistrer_elevage(data: FormulaireElevage):
    valider_arrondissement(data.arrondissement)
    try:
        doc_ref = db.collection("collectes_elevage").document()
        donnees = data.dict()
        donnees["id_document"] = doc_ref.id
        doc_ref.set(donnees)
        return {"status": "Succès (Firebase)", "message": "Fiche Élevage enregistrée", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collecte/industrie")
def enregistrer_industrie(data: FormulaireIndustrie):
    valider_arrondissement(data.arrondissement)
    try:
        doc_ref = db.collection("collectes_industries").document()
        donnees = data.dict()
        donnees["id_document"] = doc_ref.id
        doc_ref.set(donnees)
        return {"status": "Succès (Firebase)", "message": "Fiche Industrie enregistrée", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/statistiques/{section}")
def obtenir_statistiques(section: str):
    collections_valides = ["collectes_peche", "collectes_elevage", "collectes_industries"]
    if section not in collections_valides:
        raise HTTPException(status_code=400, detail="Section statistique invalide.")
    try:
        docs = db.collection(section).stream()
        liste_donnees = [doc.to_dict() for doc in docs]
        return {"section": section, "total_enregistrements": len(liste_donnees), "donnees": liste_donnees}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
