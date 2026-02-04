import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime

# Configuration du bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté et prêt !')
    print(f'ID: {bot.user.id}')
    print('------')

@bot.command(name='backup')
@commands.has_permissions(administrator=True)
async def backup_server(ctx):
    """Sauvegarde la configuration complète du serveur"""
    
    guild = ctx.guild
    msg = await ctx.send("🔄 Sauvegarde en cours... Cela peut prendre quelques instants.")
    
    # Structure de données pour la sauvegarde
    backup_data = {
        'server_name': guild.name,
        'server_icon_url': str(guild.icon.url) if guild.icon else None,
        'backup_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'roles': [],
        'categories': [],
        'channels': [],
        'afk_timeout': guild.afk_timeout,
        'verification_level': str(guild.verification_level)
    }
    
    # Sauvegarder les rôles (sans @everyone)
    for role in guild.roles:
        if role.name != "@everyone":
            backup_data['roles'].append({
                'name': role.name,
                'permissions': role.permissions.value,
                'color': role.color.value,
                'hoist': role.hoist,
                'mentionable': role.mentionable,
                'position': role.position
            })
    
    # Sauvegarder les catégories et leurs channels
    for category in guild.categories:
        category_data = {
            'name': category.name,
            'position': category.position,
            'overwrites': []
        }
        
        # Permissions de la catégorie
        for target, overwrite in category.overwrites.items():
            if isinstance(target, discord.Role):
                category_data['overwrites'].append({
                    'type': 'role',
                    'name': target.name,
                    'permissions': {
                        'allow': overwrite.pair()[0].value,
                        'deny': overwrite.pair()[1].value
                    }
                })
        
        backup_data['categories'].append(category_data)
        
        # Sauvegarder les channels de cette catégorie
        for channel in category.channels:
            channel_data = {
                'name': channel.name,
                'type': str(channel.type),
                'category': category.name,
                'position': channel.position,
                'overwrites': []
            }
            
            # Ajouter les propriétés spécifiques au type de channel
            if isinstance(channel, discord.TextChannel):
                channel_data['topic'] = channel.topic
                channel_data['slowmode_delay'] = channel.slowmode_delay
                channel_data['nsfw'] = channel.nsfw
            elif isinstance(channel, discord.VoiceChannel):
                channel_data['bitrate'] = channel.bitrate
                channel_data['user_limit'] = channel.user_limit
            
            # Permissions du channel
            for target, overwrite in channel.overwrites.items():
                if isinstance(target, discord.Role):
                    channel_data['overwrites'].append({
                        'type': 'role',
                        'name': target.name,
                        'permissions': {
                            'allow': overwrite.pair()[0].value,
                            'deny': overwrite.pair()[1].value
                        }
                    })
            
            backup_data['channels'].append(channel_data)
    
    # Sauvegarder les channels sans catégorie
    for channel in guild.channels:
        if channel.category is None and not isinstance(channel, discord.CategoryChannel):
            channel_data = {
                'name': channel.name,
                'type': str(channel.type),
                'category': None,
                'position': channel.position,
                'overwrites': []
            }
            
            if isinstance(channel, discord.TextChannel):
                channel_data['topic'] = channel.topic
                channel_data['slowmode_delay'] = channel.slowmode_delay
                channel_data['nsfw'] = channel.nsfw
            elif isinstance(channel, discord.VoiceChannel):
                channel_data['bitrate'] = channel.bitrate
                channel_data['user_limit'] = channel.user_limit
            
            for target, overwrite in channel.overwrites.items():
                if isinstance(target, discord.Role):
                    channel_data['overwrites'].append({
                        'type': 'role',
                        'name': target.name,
                        'permissions': {
                            'allow': overwrite.pair()[0].value,
                            'deny': overwrite.pair()[1].value
                        }
                    })
            
            backup_data['channels'].append(channel_data)
    
    # Sauvegarder dans un fichier JSON
    filename = f"backup_{guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=4, ensure_ascii=False)
    
    await msg.edit(content=f"✅ Sauvegarde terminée !\n📁 Fichier: `{filename}`\n"
                           f"📊 {len(backup_data['roles'])} rôles, "
                           f"{len(backup_data['categories'])} catégories, "
                           f"{len(backup_data['channels'])} channels sauvegardés.")
    
    # Envoyer le fichier
    await ctx.send(file=discord.File(filename))

@bot.command(name='restore')
@commands.has_permissions(administrator=True)
async def restore_server(ctx, filename: str = None):
    """Restaure la configuration d'un serveur à partir d'une sauvegarde"""
    
    if not filename:
        await ctx.send("❌ Veuillez spécifier le nom du fichier de sauvegarde.\n"
                      "Usage: `!restore nom_du_fichier.json`")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
    except FileNotFoundError:
        await ctx.send(f"❌ Fichier `{filename}` introuvable.")
        return
    except json.JSONDecodeError:
        await ctx.send(f"❌ Erreur lors de la lecture du fichier. Format JSON invalide.")
        return
    
    guild = ctx.guild
    msg = await ctx.send("🔄 Restauration en cours... Cela peut prendre plusieurs minutes.")
    
    # Dictionnaire pour mapper les anciens noms de rôles aux nouveaux objets
    role_map = {}
    
    # Créer les rôles
    await msg.edit(content="🔄 Création des rôles...")
    for role_data in sorted(backup_data['roles'], key=lambda x: x['position']):
        try:
            new_role = await guild.create_role(
                name=role_data['name'],
                permissions=discord.Permissions(role_data['permissions']),
                color=discord.Color(role_data['color']),
                hoist=role_data['hoist'],
                mentionable=role_data['mentionable']
            )
            role_map[role_data['name']] = new_role
            await asyncio.sleep(0.5)  # Éviter le rate limit
        except Exception as e:
            print(f"Erreur lors de la création du rôle {role_data['name']}: {e}")
    
    # Créer les catégories
    await msg.edit(content="🔄 Création des catégories...")
    category_map = {}
    for cat_data in sorted(backup_data['categories'], key=lambda x: x['position']):
        try:
            overwrites = {}
            for ow in cat_data['overwrites']:
                if ow['name'] in role_map:
                    role = role_map[ow['name']]
                    overwrites[role] = discord.PermissionOverwrite.from_pair(
                        discord.Permissions(ow['permissions']['allow']),
                        discord.Permissions(ow['permissions']['deny'])
                    )
            
            new_category = await guild.create_category(
                name=cat_data['name'],
                overwrites=overwrites
            )
            category_map[cat_data['name']] = new_category
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Erreur lors de la création de la catégorie {cat_data['name']}: {e}")
    
    # Créer les channels
    await msg.edit(content="🔄 Création des channels...")
    for chan_data in sorted(backup_data['channels'], key=lambda x: x['position']):
        try:
            overwrites = {}
            for ow in chan_data['overwrites']:
                if ow['name'] in role_map:
                    role = role_map[ow['name']]
                    overwrites[role] = discord.PermissionOverwrite.from_pair(
                        discord.Permissions(ow['permissions']['allow']),
                        discord.Permissions(ow['permissions']['deny'])
                    )
            
            category = category_map.get(chan_data['category']) if chan_data['category'] else None
            
            if 'text' in chan_data['type']:
                await guild.create_text_channel(
                    name=chan_data['name'],
                    category=category,
                    topic=chan_data.get('topic'),
                    slowmode_delay=chan_data.get('slowmode_delay', 0),
                    nsfw=chan_data.get('nsfw', False),
                    overwrites=overwrites
                )
            elif 'voice' in chan_data['type']:
                await guild.create_voice_channel(
                    name=chan_data['name'],
                    category=category,
                    bitrate=min(chan_data.get('bitrate', 64000), guild.bitrate_limit),
                    user_limit=chan_data.get('user_limit', 0),
                    overwrites=overwrites
                )
            
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Erreur lors de la création du channel {chan_data['name']}: {e}")
    
    await msg.edit(content=f"✅ Restauration terminée !\n"
                           f"📊 Serveur restauré depuis: `{backup_data['server_name']}`\n"
                           f"📅 Date de sauvegarde: {backup_data['backup_date']}")

@bot.command(name='info')
async def backup_info(ctx, filename: str = None):
    """Affiche les informations d'une sauvegarde sans la restaurer"""
    
    if not filename:
        await ctx.send("❌ Veuillez spécifier le nom du fichier de sauvegarde.\n"
                      "Usage: `!info nom_du_fichier.json`")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        embed = discord.Embed(
            title="📋 Informations de la sauvegarde",
            color=discord.Color.blue()
        )
        embed.add_field(name="Serveur", value=backup_data['server_name'], inline=False)
        embed.add_field(name="Date", value=backup_data['backup_date'], inline=False)
        embed.add_field(name="Rôles", value=str(len(backup_data['roles'])), inline=True)
        embed.add_field(name="Catégories", value=str(len(backup_data['categories'])), inline=True)
        embed.add_field(name="Channels", value=str(len(backup_data['channels'])), inline=True)
        
        await ctx.send(embed=embed)
    except FileNotFoundError:
        await ctx.send(f"❌ Fichier `{filename}` introuvable.")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

@backup_server.error
@restore_server.error
async def permission_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous devez avoir les permissions d'administrateur pour utiliser cette commande.")

@bot.command(name='help_backup')
async def help_command(ctx):
    """Affiche l'aide pour le bot"""
    
    embed = discord.Embed(
        title="🤖 Bot de Sauvegarde de Serveur Discord",
        description="Ce bot permet de sauvegarder et restaurer la configuration de vos serveurs Discord.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="!backup",
        value="Sauvegarde le serveur actuel (rôles, channels, permissions)\n"
              "**Requis:** Permissions administrateur",
        inline=False
    )
    
    embed.add_field(
        name="!restore <fichier.json>",
        value="Restaure un serveur depuis une sauvegarde\n"
              "**Requis:** Permissions administrateur\n"
              "**Exemple:** `!restore backup_123456_20240101_120000.json`",
        inline=False
    )
    
    embed.add_field(
        name="!info <fichier.json>",
        value="Affiche les informations d'une sauvegarde\n"
              "**Exemple:** `!info backup_123456_20240101_120000.json`",
        inline=False
    )
    
    embed.add_field(
        name="!help_backup",
        value="Affiche ce message d'aide",
        inline=False
    )
    
    embed.set_footer(text="⚠️ Utilisez uniquement sur vos propres serveurs ou avec autorisation !")
    
    await ctx.send(embed=embed)

# Remplacez 'VOTRE_TOKEN_ICI' par votre token de bot Discord
if __name__ == "__main__":
    TOKEN = 'MTQ2ODU1MTIxMzUwNjIzNjQ4Mg.GGftsB.J-_qqzrjdmo5g8o0IQhq08av88R3bqiQXXBXi0'
    bot.run(TOKEN)
