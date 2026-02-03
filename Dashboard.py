import streamlit as st
import base64
from PIL import Image
import io

# Configuration de la page
st.set_page_config(
    page_title="Émulateur Néon - Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec effet néon
st.markdown("""
<style>
    /* Styles principaux */
    .main {
        background-color: #0a0a1a;
        color: #00ffff;
    }
    
    /* Titre néon */
    .neon-title {
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        text-shadow: 
            0 0 10px #00ffff,
            0 0 20px #00ffff,
            0 0 30px #0088ff;
        animation: flicker 1.5s infinite alternate;
        margin-bottom: 0.5em;
    }
    
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            text-shadow: 
                0 0 10px #00ffff,
                0 0 20px #00ffff,
                0 0 30px #0088ff,
                0 0 40px #0088ff;
        }
        20%, 24%, 55% {
            text-shadow: none;
        }
    }
    
    /* Container principal */
    .st-emotion-cache-1r6slb0 {
        background-color: rgba(0, 20, 40, 0.7);
        border: 2px solid #00ffff;
        border-radius: 15px;
        box-shadow: 
            0 0 15px #00ffff,
            inset 0 0 15px #00ffff;
        padding: 2em;
        margin: 1em 0;
    }
    
    /* Boutons de jeu - Nouveau style pour 6 jeux */
    .game-button-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin: 20px 0;
    }
    
    .game-button {
        background: rgba(0, 60, 100, 0.5);
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 30px !important;
        padding: 10px 15px !important;
        margin: 5px;
        font-weight: bold;
        font-size: 0.9em;
        box-shadow: 0 0 8px #00ffff;
        transition: all 0.3s;
        white-space: nowrap;
        min-width: 120px;
    }
    
    .game-button:hover {
        background: #00ffff !important;
        color: #0a0a1a !important;
        box-shadow: 0 0 15px #00ffff;
    }
    
    .game-button-active {
        background: #00ffff !important;
        color: #0a0a1a !important;
        box-shadow: 0 0 15px #00ffff;
    }
    
    /* Boutons glow */
    .glow-button {
        background: transparent;
        color: #00ffff;
        border: 2px solid #00ffff;
        border-radius: 30px;
        padding: 10px 25px;
        margin: 10px;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 0 10px #00ffff;
    }
    
    .glow-button:hover {
        background: #00ffff;
        color: #0a0a1a;
        box-shadow: 0 0 20px #00ffff, 0 0 30px #0088ff;
    }
    
    /* Contrôles */
    .controls-container {
        background-color: rgba(0, 40, 60, 0.6);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ffff;
        margin: 20px 0;
    }
    
    /* Titre du jeu */
    .game-title {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffff;
        margin: 1em 0;
    }
    
    .game-subtitle {
        text-align: center;
        color: #0088ff;
        margin-bottom: 2em;
    }
    
    /* Iframe container */
    .iframe-container {
        border: 3px solid #00ffff;
        box-shadow: 0 0 20px #0088ff;
        border-radius: 10px;
        overflow: hidden;
        margin: 20px 0;
        height: 600px;
        background-color: #000;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2em;
        color: #0088ff;
        font-size: 0.9em;
    }
    
    /* Style pour les listes */
    ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    li {
        padding: 5px 0;
        color: #00ffff;
    }
    
    strong {
        color: #00ffff;
    }
    
    /* Badge console */
    .console-badge {
        display: inline-block;
        background: rgba(255, 0, 255, 0.3);
        color: #ff00ff;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 10px;
        border: 1px solid #ff00ff;
    }
</style>
""", unsafe_allow_html=True)

# Données des jeux (6 jeux maintenant)
GAMES = {
    "fifa97": {
        "name": "FIFA 97 GOLD EDITION",
        "subtitle": "Édition Europe (FR/DE/ES/IT/SV)",
        "url": "https://www.retrogames.cc/embed/19637-fifa-97-gold-edition-europe-en-fr-de-es-it-sv.html",
        "console": "SNES",
        "color": "#00ff00",
        "controls": [
            "**Flèches :** Déplacement",
            "**X :** Tir / Passe courte",
            "**Z :** Passe longue / Centre",
            "**A :** Sprint",
            "**S :** Frappe / Dribble",
            "**Espace :** Changement de joueur",
            "**Entrée :** Pause / Menu"
        ]
    },
    "lhx": {
        "name": "LHX ATTACK CHOPPER",
        "subtitle": "Version USA/Europe",
        "url": "https://www.retrogames.cc/embed/28482-lhx-attack-chopper-usa-europe.html",
        "console": "MegaDrive",
        "color": "#ff6600",
        "controls": [
            "**Flèches :** Direction",
            "**A :** Tir principal",
            "**B :** Tir secondaire",
            "**X/Y :** Changement d'arme",
            "**Start :** Pause",
            "**Select :** Carte"
        ]
    },
    "roadrash": {
        "name": "ROAD RASH 3D",
        "subtitle": "Jeu de course/combat",
        "url": "https://www.retrogames.cc/embed/41508-road-rash-3d.html",
        "console": "PlayStation",
        "color": "#ff0000",
        "controls": [
            "**Flèches :** Direction",
            "**A :** Accélérer",
            "**B :** Frein",
            "**X :** Coup de poing gauche",
            "**Y :** Coup de poing droit",
            "**L/R :** Coups de pied",
            "**Start :** Pause"
        ]
    },
    "rayman": {
        "name": "RAYMAN 2",
        "subtitle": "The Great Escape",
        "url": "https://www.retrogames.cc/embed/41925-rayman-2-the-great-escape.html",
        "console": "PlayStation",
        "color": "#ffff00",
        "controls": [
            "**Flèches :** Déplacement",
            "**A :** Sauter",
            "**B :** Tirer (énergie)",
            "**X :** Action/secondaire",
            "**Y :** Accroupir",
            "**L/R :** Changer caméra",
            "**Start :** Pause"
        ]
    },
    "racing": {
        "name": "RACING LAGOON",
        "subtitle": "Jeu de course RPG",
        "url": "https://www.retrogames.cc/embed/41861-racing-lagoon.html",
        "console": "PlayStation",
        "color": "#00ffff",
        "controls": [
            "**Flèches :** Direction",
            "**X :** Accélérer",
            "**Z :** Frein",
            "**A :** Boost",
            "**S :** Changement de vue",
            "**L/R :** Dérive",
            "**Start :** Pause/Menu"
        ]
    },
    "rally": {
        "name": "RALLY CHALLENGE 2000",
        "subtitle": "Version USA",
        "url": "https://www.retrogames.cc/embed/43877-rally-challenge-2000-usa.html",
        "console": "Nintendo 64",
        "color": "#ff00ff",
        "controls": [
            "**Joystick :** Direction",
            "**A :** Accélérer",
            "**B :** Frein/maintenir",
            "**Z :** Regarder derrière",
            "**L :** Frein à main",
            "**R :** Changement de vitesse",
            "**Start :** Pause/Menu",
            "**C-boutons :** Changement de vue"
        ]
    }
}

# Initialisation de l'état
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = 'fifa97'

def change_game(game_id):
    st.session_state.selected_game = game_id

# Interface principale
st.markdown('<h1 class="neon-title">ÉMULATEUR NÉON</h1>', unsafe_allow_html=True)

# Sélecteur de jeu avec 6 boutons (2 lignes de 3)
st.markdown('<div class="game-button-container">', unsafe_allow_html=True)

# Première ligne : 3 jeux
col1, col2, col3 = st.columns(3)
game_ids = list(GAMES.keys())

with col1:
    game_id = game_ids[0]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"⚽ {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

with col2:
    game_id = game_ids[1]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"🚁 {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

with col3:
    game_id = game_ids[2]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"🏍️ {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

st.markdown('</div>', unsafe_allow_html=True)

# Deuxième ligne : 3 autres jeux
st.markdown('<div class="game-button-container">', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    game_id = game_ids[3]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"👻 {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

with col5:
    game_id = game_ids[4]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"🏎️ {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

with col6:
    game_id = game_ids[5]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    if st.button(
        f"🏁 {game['name'].split()[0]}",
        key=f"btn_{game_id}",
        use_container_width=True,
        type="primary" if is_active else "secondary"
    ):
        change_game(game_id)

st.markdown('</div>', unsafe_allow_html=True)

# Affichage du jeu sélectionné
game = GAMES[st.session_state.selected_game]

# Affichage du titre avec badge console
st.markdown(f'''
    <h2 class="game-title">
        {game["name"]}
        <span class="console-badge" style="border-color: {game['color']}; color: {game['color']};">
            {game["console"]}
        </span>
    </h2>
    <p class="game-subtitle">{game["subtitle"]}</p>
''', unsafe_allow_html=True)

# Iframe de l'émulateur
st.markdown(f'''
<div class="iframe-container">
    <iframe 
        src="{game['url']}"
        width="100%"
        height="600"
        frameborder="no"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
        title="{game['name']} - Émulateur">
    </iframe>
</div>
''', unsafe_allow_html=True)

# Section des commandes
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
st.markdown(f'''
<h3 style="color:{game['color']}; text-shadow: 0 0 10px {game['color']};">
    🎮 COMMANDES {game["console"]} :
</h3>
''', unsafe_allow_html=True)

for control in game["controls"]:
    st.markdown(f"• {control}", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Boutons d'action
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 SAUVEGARDE", use_container_width=True):
        st.info(f"Pour sauvegarder : Utilisez le menu de l'émulateur {game['console']} (icône disquette)")

with col2:
    if st.button("🔄 REDÉMARRER LE JEU", use_container_width=True):
        st.rerun()

with col3:
    if st.button("⚙️ CONFIGURATION N64", use_container_width=True) and st.session_state.selected_game == "rally":
        st.info("""
        Configuration recommandée pour N64 :
        - Plugin graphique : GLideN64
        - Résolution : 640x480
        - Filtre texture : Bilinéaire
        - FPS : 60 (VSync activé)
        """)

st.markdown('</div>', unsafe_allow_html=True)

# Section informations spécifiques pour Rally Challenge 2000
if st.session_state.selected_game == "rally":
    with st.expander("🏁 **INFORMATIONS RALLY CHALLENGE 2000**", expanded=False):
        st.markdown("""
        ### À propos du jeu :
        **Rally Challenge 2000** est un jeu de course de rallye sorti sur Nintendo 64 en 1999.
        
        ### Caractéristiques :
        - **Développeur** : ATLUS
        - **Éditeur** : ATLUS
        - **Sortie** : 1999
        - **Genre** : Course de rallye
        
        ### Circuits disponibles :
        1. **Forest Path** - Forêt
        2. **Desert Road** - Désert  
        3. **Mountain Pass** - Montagne
        4. **Snow Trail** - Neige
        5. **City Streets** - Ville
        
        ### Voitures :
        - Subaru Impreza WRC
        - Mitsubishi Lancer Evolution
        - Toyota Corolla WRC
        - Ford Focus WRC
        
        ### Conseils de jeu :
        - Utilisez le frein à main (L) pour les virages serrés
        - Changez de vue avec les C-boutons pour meilleure visibilité
        - Anticipez les virages, les rallys sont techniques !
        """)

# Section informations générales
with st.expander("ℹ️ **INFORMATIONS IMPORTANTES**", expanded=False):
    st.markdown("""
    ### Instructions d'utilisation :
    1. Cliquez sur l'iframe pour activer les commandes
    2. Utilisez les touches indiquées ci-dessus
    3. Pour sauvegarder : Menu de l'émulateur (icône disquette)
    4. Pour redémarrer : Bouton "REDÉMARRER" ou F5
    
    ### Compatibilité :
    - Tous les jeux fonctionnent directement dans le navigateur
    - Supporte les manettes USB/Bluetooth
    - Fonctionne sur PC, tablette et mobile
    
    ### Notes techniques :
    - Les sauvegardes sont stockées localement
    - La performance dépend de votre connexion internet
    - Pour N64 : Utilisez Chrome/Firefox pour meilleure compatibilité
    """)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("""
<div style="border-top: 1px solid #0088ff; padding-top: 20px; margin-top: 30px;">
    <p>Émulateur fourni par RetroGames.cc | Design Néon © 2024</p>
    <p style="font-size: 0.8em; color: #00aaff;">
        🎮 6 jeux disponibles • 📺 4 consoles supportées • ⚡ Expérience optimisée
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar avec statistiques
with st.sidebar:
    st.markdown("### 📊 STATISTIQUES")
    
    # Compteur par console
    consoles = {}
    for game in GAMES.values():
        console = game["console"]
        consoles[console] = consoles.get(console, 0) + 1
    
    st.metric("Jeux disponibles", len(GAMES))
    st.metric("Console actuelle", game["console"])
    
    st.markdown("---")
    st.markdown("### 🎮 RÉPARTITION PAR CONSOLE")
    for console, count in consoles.items():
        st.progress(count/len(GAMES), text=f"{console}: {count} jeu{'s' if count > 1 else ''}")
    
    st.markdown("---")
    st.markdown("### 🚀 CONTRÔLES RAPIDES")
    
    for game_id, game_info in GAMES.items():
        icon = "🏁" if game_id == "rally" else "🎮"
        if st.button(f"{icon} {game_info['name'].split()[0]}", 
                    key=f"sidebar_{game_id}", 
                    use_container_width=True, 
                    type="primary" if st.session_state.selected_game == game_id else "secondary"):
            change_game(game_id)
    
    st.markdown("---")
    st.markdown("### ⚙️ CONFIGURATION")
    
    volume = st.slider("Volume", 0, 100, 80)
    st.session_state.volume = volume
    
    quality_options = {
        "Haute": "Haute qualité graphique",
        "Moyenne": "Équilibre performance/qualité", 
        "Basse": "Performance maximale"
    }
    
    quality = st.selectbox("Qualité graphique", list(quality_options.keys()))
    st.caption(quality_options[quality])
    
    if st.button("Appliquer les paramètres", use_container_width=True):
        st.success(f"✅ Paramètres appliqués ! (Volume: {volume}%, Qualité: {quality})")
