#!/usr/bin/env python3
"""
Script utilitaire pour encoder votre token Discord en Base64
"""

import base64
import os

def encode_token():
    """Encode un token Discord en Base64"""
    
    print("=" * 60)
    print("🔐 ENCODEUR DE TOKEN DISCORD EN BASE64")
    print("=" * 60)
    print()
    print("⚠️  ATTENTION : Ne partagez JAMAIS votre token avec personne !")
    print()
    
    # Demander le token
    token = input("Entrez votre token Discord : ").strip()
    
    if not token:
        print("❌ Token vide. Abandon.")
        return
    
    # Encoder en Base64
    token_bytes = token.encode('utf-8')
    encoded_token = base64.b64encode(token_bytes).decode('utf-8')
    
    print()
    print("✅ Token encodé avec succès !")
    print()
    print("=" * 60)
    print("Votre token encodé en Base64 :")
    print("-" * 60)
    print(encoded_token)
    print("=" * 60)
    print()
    
    # Créer ou mettre à jour le fichier .env
    response = input("Voulez-vous créer/mettre à jour le fichier .env automatiquement ? (o/n) : ").strip().lower()
    
    if response in ['o', 'oui', 'y', 'yes']:
        env_content = f"""# Configuration du Bot Discord
# Token encodé en Base64 pour plus de sécurité

DISCORD_TOKEN_B64={encoded_token}

# ⚠️ Ne partagez jamais ce fichier !
# Ajoutez .env à votre .gitignore
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print()
        print("✅ Fichier .env créé avec succès !")
        print("📁 Localisation : .env")
        print()
        print("⚠️  N'oubliez pas d'ajouter '.env' à votre .gitignore !")
    else:
        print()
        print("📝 Copiez le token encodé ci-dessus et ajoutez-le manuellement dans votre fichier .env :")
        print()
        print(f"DISCORD_TOKEN_B64={encoded_token}")
    
    print()
    print("=" * 60)
    print("🚀 Vous pouvez maintenant lancer le bot avec :")
    print("   python discord_backup_bot.py")
    print("=" * 60)

def decode_token():
    """Décode un token Base64 (pour vérification)"""
    
    print()
    print("=" * 60)
    print("🔓 DÉCODEUR DE TOKEN BASE64")
    print("=" * 60)
    print()
    
    encoded = input("Entrez le token encodé en Base64 : ").strip()
    
    if not encoded:
        print("❌ Token vide. Abandon.")
        return
    
    try:
        decoded_bytes = base64.b64decode(encoded)
        decoded_token = decoded_bytes.decode('utf-8')
        
        print()
        print("✅ Token décodé avec succès !")
        print()
        print("=" * 60)
        print("Token original :")
        print("-" * 60)
        print(decoded_token)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erreur lors du décodage : {e}")

def main():
    """Menu principal"""
    
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        🔐 UTILITAIRE TOKEN DISCORD (BASE64)            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("Que voulez-vous faire ?")
    print()
    print("1. Encoder un token en Base64")
    print("2. Décoder un token Base64 (vérification)")
    print("3. Quitter")
    print()
    
    choice = input("Votre choix (1-3) : ").strip()
    
    if choice == '1':
        encode_token()
    elif choice == '2':
        decode_token()
    elif choice == '3':
        print("👋 Au revoir !")
    else:
        print("❌ Choix invalide.")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur. Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
