# 🤖 Bot Discord - Sauvegarde & Restauration de Serveur

Bot Discord permettant de sauvegarder et restaurer la configuration complète de vos serveurs Discord (rôles, channels, permissions, etc.).

## ⚠️ IMPORTANT - Usage Légal

**Ce bot doit être utilisé UNIQUEMENT sur :**
- Vos propres serveurs Discord
- Des serveurs où vous avez reçu l'autorisation explicite du propriétaire

L'utilisation de ce bot pour cloner des serveurs sans autorisation viole les conditions d'utilisation de Discord et peut entraîner un bannissement.

## 🌟 Fonctionnalités

- ✅ Sauvegarde complète des rôles (permissions, couleurs, positions)
- ✅ Sauvegarde des catégories avec leurs permissions
- ✅ Sauvegarde de tous les channels (texte et vocal)
- ✅ Sauvegarde des permissions spécifiques à chaque channel
- ✅ Restauration automatisée sur un nouveau serveur
- ✅ Fichiers de sauvegarde au format JSON lisible
- ✅ Protection par permissions administrateur

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un compte Discord Developer avec un bot créé
- Permissions administrateur sur les serveurs où vous utiliserez le bot

## 🚀 Installation

### 1. Cloner ou télécharger les fichiers

Assurez-vous d'avoir tous les fichiers dans le même dossier :
- `discord_backup_bot.py` - Le bot principal
- `requirements.txt` - Les dépendances
- `.env.example` - Exemple de configuration
- `encode_token.py` - Script pour encoder votre token en Base64
- `.gitignore` - Protection des fichiers sensibles
- `README.md` - Cette documentation

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Créer votre bot Discord

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur "New Application"
3. Donnez un nom à votre application
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. Activez les "Privileged Gateway Intents" suivants :
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT
7. Copiez le token du bot

### 4. Configurer le token (ENCODÉ EN BASE64)

Le bot utilise un token encodé en Base64 pour plus de sécurité.

**Méthode 1 : Utiliser le script automatique (recommandé)**

```bash
python encode_token.py
```

Le script vous demandera votre token Discord, l'encodera en Base64, et créera automatiquement le fichier `.env`.

**Méthode 2 : Encoder manuellement**

1. Encodez votre token en Base64 :
   - En Python : `python -c "import base64; print(base64.b64encode(b'VOTRE_TOKEN').decode())"`
   - En ligne : utilisez un encodeur Base64 en ligne

2. Créez un fichier `.env` :
```bash
cp .env.example .env
```

3. Éditez `.env` et ajoutez votre token encodé :
```
DISCORD_TOKEN_B64=dm90cmVfdG9rZW5fZW5jb2Rl
```

⚠️ **Important** : N'oubliez pas d'ajouter `.env` à votre `.gitignore` (déjà fait si vous utilisez le fichier fourni) !

### 5. Inviter le bot sur votre serveur

1. Retournez sur https://discord.com/developers/applications
2. Sélectionnez votre application
3. Allez dans "OAuth2" > "URL Generator"
4. Cochez les scopes :
   - ✅ bot
5. Cochez les permissions du bot :
   - ✅ Administrator (ou toutes les permissions nécessaires)
6. Copiez l'URL générée et ouvrez-la dans votre navigateur
7. Sélectionnez le serveur où inviter le bot

## 💻 Utilisation

### Démarrer le bot

```bash
python discord_backup_bot.py
```

### Commandes disponibles

#### `!backup`
Sauvegarde le serveur actuel dans un fichier JSON.

**Exemple :**
```
!backup
```

**Résultat :** Crée un fichier `backup_[ID_SERVEUR]_[DATE].json` contenant toute la configuration.

---

#### `!restore <fichier.json>`
Restaure la configuration d'un serveur depuis une sauvegarde.

**Exemple :**
```
!restore backup_123456789_20240204_153000.json
```

**⚠️ Attention :** Cette commande créera tous les rôles et channels de la sauvegarde sur le serveur actuel. Utilisez de préférence sur un serveur vide.

---

#### `!info <fichier.json>`
Affiche les informations d'une sauvegarde sans la restaurer.

**Exemple :**
```
!info backup_123456789_20240204_153000.json
```

---

#### `!help_backup`
Affiche l'aide du bot dans Discord.

## 📁 Structure des fichiers de sauvegarde

Les sauvegardes sont au format JSON et contiennent :

```json
{
    "server_name": "Nom du serveur",
    "backup_date": "2024-02-04 15:30:00",
    "roles": [...],
    "categories": [...],
    "channels": [...],
    "afk_timeout": 300,
    "verification_level": "medium"
}
```

## ⚙️ Configuration avancée

### Modifier le préfixe des commandes

Dans `discord_backup_bot.py`, ligne 11 :

```python
bot = commands.Bot(command_prefix='!', intents=intents)
```

Changez `'!'` par le préfixe de votre choix (ex: `'?'`, `'/'`, etc.)

### Limites et délais

Pour éviter le rate limiting de Discord, le bot attend 0.5 seconde entre chaque création de rôle/channel. Vous pouvez ajuster ce délai dans le code si nécessaire.

## 🛡️ Sécurité

- **Ne partagez JAMAIS votre token de bot** - C'est comme un mot de passe
- Le token est encodé en Base64 dans le fichier `.env` pour éviter qu'il soit visible en clair
- Ajoutez `.env` à votre `.gitignore` (déjà inclus dans le fichier fourni)
- Ne donnez les permissions administrateur qu'aux personnes de confiance
- Vérifiez toujours le contenu d'une sauvegarde avec `!info` avant de la restaurer

**Note sur Base64** : L'encodage Base64 n'est PAS un chiffrement, c'est simplement de l'obscurcissement. Il empêche simplement que le token soit visible directement dans les fichiers. Pour une vraie sécurité, ne partagez jamais votre fichier `.env` et gardez vos tokens secrets.

## 🐛 Résolution des problèmes

### Le bot ne répond pas
- Vérifiez que le bot est en ligne (il doit apparaître dans la liste des membres)
- Vérifiez que les intents sont activés dans le Developer Portal
- Vérifiez les permissions du bot sur le serveur

### Erreur "Missing Permissions"
- Le bot doit avoir les permissions administrateur
- Vérifiez que vous avez vous-même les permissions administrateur

### Certains éléments ne sont pas restaurés
- Discord impose des limites (ex: bitrate maximum selon le niveau du serveur)
- Le bot ajuste automatiquement certaines valeurs pour respecter ces limites

### Rate Limit / Trop de requêtes
- Le processus de restauration peut prendre plusieurs minutes pour les gros serveurs
- Soyez patient et ne lancez pas plusieurs commandes en même temps

## 📝 Notes importantes

- Les messages des channels ne sont pas sauvegardés (seulement la structure)
- Les emojis personnalisés ne sont pas sauvegardés
- Les webhooks ne sont pas sauvegardés
- Les invitations ne sont pas sauvegardées
- Les membres et leurs rôles ne sont pas sauvegardés

## 📄 Licence

Ce code est fourni à des fins éducatives. Utilisez-le de manière responsable et respectueuse des conditions d'utilisation de Discord.

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que toutes les dépendances sont installées
2. Vérifiez que votre token est correct
3. Vérifiez les permissions du bot
4. Consultez les logs d'erreur dans la console

---

**Développé avec ❤️ pour la gestion de serveurs Discord**
