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
    
    /* Boutons de jeu */
    .game-button {
        background: rgba(0, 60, 100, 0.5);
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 30px !important;
        padding: 10px 20px !important;
        margin: 5px;
        font-weight: bold;
        box-shadow: 0 0 8px #00ffff;
        transition: all 0.3s;
        white-space: nowrap;
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
</style>
""", unsafe_allow_html=True)

# Données des jeux
GAMES = {
    "fifa97": {
        "name": "FIFA 97 GOLD EDITION",
        "subtitle": "Édition Europe (FR/DE/ES/IT/SV) - SNES",
        "url": "https://www.retrogames.cc/embed/19637-fifa-97-gold-edition-europe-en-fr-de-es-it-sv.html",
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
        "subtitle": "Version USA/Europe - MegaDrive",
        "url": "https://www.retrogames.cc/embed/28482-lhx-attack-chopper-usa-europe.html",
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
        "subtitle": "Jeu de course/combat - PlayStation",
        "url": "https://www.retrogames.cc/embed/41508-road-rash-3d.html",
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
        "subtitle": "The Great Escape - PlayStation",
        "url": "https://www.retrogames.cc/embed/41925-rayman-2-the-great-escape.html",
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
        "subtitle": "Jeu de course RPG - PlayStation",
        "url": "https://www.retrogames.cc/embed/41861-racing-lagoon.html",
        "controls": [
            "**Flèches :** Direction",
            "**X :** Accélérer",
            "**Z :** Frein",
            "**A :** Boost",
            "**S :** Changement de vue",
            "**L/R :** Dérive",
            "**Start :** Pause/Menu"
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

# Sélecteur de jeu avec colonnes
cols = st.columns(5)
game_ids = list(GAMES.keys())

for i, game_id in enumerate(game_ids):
    game = GAMES[game_id]
    with cols[i]:
        is_active = st.session_state.selected_game == game_id
        button_class = "game-button-active" if is_active else "game-button"
        if st.button(
            game["name"].split()[0],  # Affiche juste le premier mot du nom
            key=f"btn_{game_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            change_game(game_id)

# Affichage du jeu sélectionné
game = GAMES[st.session_state.selected_game]

st.markdown(f'<h2 class="game-title">{game["name"]}</h2>', unsafe_allow_html=True)
st.markdown(f'<p class="game-subtitle">{game["subtitle"]}</p>', unsafe_allow_html=True)

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
        mozallowfullscreen="true">
    </iframe>
</div>
''', unsafe_allow_html=True)

# Section des commandes
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#00ffff; text-shadow: 0 0 5px #00ffff;">COMMANDES :</h3>', unsafe_allow_html=True)

for control in game["controls"]:
    st.markdown(f"• {control}", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Boutons d'action
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 SAUVEGARDE", use_container_width=True):
        st.info("Pour sauvegarder : Utilisez le menu de l'émulateur (icône disquette dans l'interface)")

with col2:
    if st.button("🔄 REDÉMARRER", use_container_width=True):
        st.rerun()

with col3:
    if st.button("⚙️ CONFIGURATION", use_container_width=True):
        st.info("Configuration de l'émulateur disponible dans le menu intégré")

# Section informations supplémentaires
with st.expander("ℹ️ **INFORMATIONS IMPORTANTES**"):
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
    - Certains jeux peuvent nécessiter une configuration spécifique
    """)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Émulateur fourni par RetroGames.cc | Design Néon © 2024")
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar avec statistiques
with st.sidebar:
    st.markdown("### 📊 STATISTIQUES")
    st.metric("Jeux disponibles", len(GAMES))
    st.metric("Console actuelle", 
              "SNES" if st.session_state.selected_game == "fifa97" else 
              "MegaDrive" if st.session_state.selected_game == "lhx" else 
              "PlayStation")
    
    st.markdown("---")
    st.markdown("### 🎮 CONTRÔLES RAPIDES")
    
    for game_id, game_info in GAMES.items():
        if st.button(f"▶️ {game_info['name']}", key=f"sidebar_{game_id}", 
                    use_container_width=True, 
                    type="primary" if st.session_state.selected_game == game_id else "secondary"):
            change_game(game_id)
    
    st.markdown("---")
    st.markdown("### ⚙️ CONFIGURATION")
    
    volume = st.slider("Volume", 0, 100, 80)
    st.session_state.volume = volume
    
    quality = st.selectbox("Qualité graphique", ["Haute", "Moyenne", "Basse"])
    
    if st.button("Appliquer les paramètres"):
        st.success("Paramètres appliqués !")
