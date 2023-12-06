import json
import hashlib
import random
import string

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#"
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if (
            any(i.isupper() for i in password) and
            any(i.islower() for i in password) and
            any(i.isdigit() for i in password) and
            any(not i.isalnum() for i in password) and
            len(password) >= 8
        ):
            return password


def hasher_mot_de_passe(code):
    sha256 = hashlib.sha256()
    code_encode = code.encode('utf-8')
    sha256.update(code_encode)
    code_binaire = sha256.digest()
    return code_binaire

def save_code(code_hache, enregistreur_code='gestion_code_hache.json'):
    # Charger les anciens mots de passe
    try:
        with open(enregistreur_code, 'r') as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        # Si le fichier n'existe pas, initialiser data à une liste vide
        data = []

    # Convertir le code hexadécimal en une chaîne
    code_hex = code_hache.hex()

    # Vérifier si le mot de passe est déjà dans la liste
    if code_hex not in data:
        # Ajouter le nouveau mot de passe
        data.append(code_hex)

        # Enregistrer le fichier avec les mots de passe mis à jour
        with open(enregistreur_code, 'w') as fichier:
            json.dump(data, fichier)
    else:
        print("Ce mot de passe est déjà enregistré.")

def afficher_codes(enregistreur_code='gestion_code_hache.json'):
    try:
        with open(enregistreur_code, 'r') as fichier:
            print("Contenu du fichier:")
            contenu = json.load(fichier)
            for code_hache_hex in contenu:
                # Afficher le code hexadécimal
                print(code_hache_hex)
    except FileNotFoundError:
        print("Le fichier spécifié n'existe pas.")
        x = input("Voir les mdp (oui) :")
        if x == "oui":
            print("Aucun mot de passe enregistré.")

def jeux():
    print("\nbienvenue dans password")
    print("le but du jeu est de saisir un code et pour gagner, il faut respecter les étapes")
    print("\n➔ Il doit contenir au moins une lettre majuscule, au moins une lettre minuscule, au moins un chiffre, au moins un caractère spécial (!, @, #,)")

    option = input("Voulez-vous entrer un nouveau mot de passe (1) ou en générer un aléatoirement (2) ? ")

    if option == "1":
        # L'utilisateur entre son propre mot de passe
        code = input("\nVeuillez entrer votre mot de passe : ")
    elif option == "2":
        # L'utilisateur veut un mot de passe généré aléatoirement
        code = generate_random_password()
        print("\nMot de passe généré aléatoirement :", code)
    else:
        print("Option invalide. Choisissez 1 ou 2.")
        return

    # La suite du code reste inchangée
    conditions = 0
    charactere = 8

    if len(code) >= charactere:
        conditions += 1
        print("\nPremière étape validée")
    else:
        print("Première étape non validée")

    # Deuxième étape: au moins 1 majuscule
    maj = any(i.isupper() for i in code)
    if maj:
        conditions += 1
        print("Deuxième étape validée")
    else:
        print("Deuxième étape non validée")

    # Troisième étape: au moins 1 minuscule
    mini = any(i.islower() for i in code)
    if mini:
        conditions += 1
        print("Troisième étape validée")
    else:
        print("Troisième étape non validée")

    # Quatrième étape: au moins 1 chiffre
    nbr = any(i.isdigit() for i in code)
    if nbr:
        conditions += 1
        print("Quatrième étape validée")
    else:
        print("Quatrième étape non validée")

    # Cinquième étape: au moins 1 caractère spécial
    speciaux = any(not i.isalnum() for i in code)
    if speciaux:
        conditions += 1
        print("Cinquième étape validée")
    else:
        print("Cinquième étape non validée")

    print("\nVous avez rempli les", conditions, "conditions")

    if conditions == 5:
        print("\nBravo, vous avez gagné !")
        code_hache = hasher_mot_de_passe(code)
        save_code(code_hache)

        x = input("Voir les mdp (oui) :")
        if x == "oui":
            afficher_codes()

    else:
        print("\nNub, vous avez perdu !")

        code_hache = hasher_mot_de_passe(code)
        save_code(code_hache)

    return code_hache

jeux()