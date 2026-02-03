import streamlit as st
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
        font-size: 3em;
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
    .main-container {
        background-color: rgba(0, 20, 40, 0.7);
        border: 2px solid #00ffff;
        border-radius: 15px;
        box-shadow: 
            0 0 15px #00ffff,
            inset 0 0 15px #00ffff;
        padding: 1.5em;
        margin: 1em auto;
        max-width: 1200px;
    }
    
    /* Boutons de jeu - Adaptation pour 8 jeux */
    .game-button-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 6px;
        margin: 12px 0;
    }
    
    .game-button {
        background: rgba(0, 60, 100, 0.5);
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 22px !important;
        padding: 7px 10px !important;
        margin: 2px;
        font-weight: bold;
        font-size: 0.8em;
        box-shadow: 0 0 5px #00ffff;
        transition: all 0.3s;
        white-space: nowrap;
        min-width: 100px;
        flex: 1 0 auto;
        max-width: 140px;
    }
    
    .game-button:hover {
        background: #00ffff !important;
        color: #0a0a1a !important;
        box-shadow: 0 0 10px #00ffff;
    }
    
    .game-button-active {
        background: #00ffff !important;
        color: #0a0a1a !important;
        box-shadow: 0 0 10px #00ffff;
    }
    
    /* Boutons glow */
    .glow-button {
        background: transparent;
        color: #00ffff;
        border: 2px solid #00ffff;
        border-radius: 22px;
        padding: 7px 18px;
        margin: 6px;
        font-weight: bold;
        font-size: 0.85em;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 0 7px #00ffff;
    }
    
    .glow-button:hover {
        background: #00ffff;
        color: #0a0a1a;
        box-shadow: 0 0 12px #00ffff, 0 0 20px #0088ff;
    }
    
    /* Contrôles */
    .controls-container {
        background-color: rgba(0, 40, 60, 0.6);
        padding: 12px;
        border-radius: 7px;
        border: 1px solid #00ffff;
        margin: 12px 0;
    }
    
    /* Titre du jeu */
    .game-title {
        text-align: center;
        font-size: 1.7em;
        font-weight: bold;
        text-shadow: 0 0 7px #00ffff;
        margin: 0.7em 0;
    }
    
    .game-subtitle {
        text-align: center;
        color: #0088ff;
        margin-bottom: 1.3em;
        font-size: 0.9em;
    }
    
    /* Iframe container */
    .iframe-container {
        border: 3px solid #00ffff;
        box-shadow: 0 0 12px #0088ff;
        border-radius: 7px;
        overflow: hidden;
        margin: 12px 0;
        height: 500px;
        background-color: #000;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 1.3em;
        color: #0088ff;
        font-size: 0.75em;
        padding-top: 12px;
        border-top: 1px solid #0088ff;
    }
    
    /* Style pour les listes */
    ul {
        list-style-type: none;
        padding-left: 0;
        margin: 8px 0;
    }
    
    li {
        padding: 3px 0;
        color: #00ffff;
        font-size: 0.85em;
    }
    
    strong {
        color: #00ffff;
    }
    
    /* Badge console */
    .console-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.3);
        color: #00ffff;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 0.65em;
        margin-left: 8px;
        border: 1px solid #00ffff;
        vertical-align: middle;
    }
    
    /* Badge arcade spécial */
    .arcade-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.3);
        color: #ffd700;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 0.65em;
        margin-left: 8px;
        border: 1px solid #ffd700;
        vertical-align: middle;
        animation: gold-pulse 2s infinite;
    }
    
    @keyframes gold-pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    /* Amélioration responsive */
    @media (max-width: 768px) {
        .game-button {
            min-width: 85px;
            font-size: 0.7em;
            padding: 5px 7px !important;
        }
        
        .iframe-container {
            height: 380px;
        }
        
        .neon-title {
            font-size: 2.3em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Données des jeux (8 jeux maintenant)
GAMES = {
    "fifa97": {
        "name": "FIFA 97 GOLD EDITION",
        "subtitle": "Édition Europe (FR/DE/ES/IT/SV)",
        "url": "https://www.retrogames.cc/embed/19637-fifa-97-gold-edition-europe-en-fr-de-es-it-sv.html",
        "console": "SNES",
        "color": "#00ff00",
        "icon": "⚽",
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
        "icon": "🚁",
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
        "icon": "🏍️",
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
        "icon": "👻",
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
        "icon": "🏎️",
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
        "icon": "🏁",
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
    },
    "nfscarbon": {
        "name": "NEED FOR SPEED CARBON",
        "subtitle": "Own the City (Europe) (En,Fr,De,Es,It)",
        "url": "https://www.retrogames.cc/embed/43878-need-for-speed-carbon-own-the-city-europe-en-fr-de-es-it.html",
        "console": "Nintendo DS",
        "color": "#ff3300",
        "icon": "🚗",
        "controls": [
            "**Stylet/Flèches :** Direction",
            "**A :** Accélérer",
            "**B :** Frein/Dérive",
            "**X :** Nitro (boost)",
            "**Y :** Changement de vue",
            "**L :** Regarder derrière",
            "**R :** Frein à main",
            "**Start :** Pause/Menu",
            "**Select :** Carte/Radar",
            "**Écran tactile :** Menu/Gestion équipe"
        ]
    },
    "streethoop": {
        "name": "STREET HOOP",
        "subtitle": "Street Slam / Dunk Dream (Arcade)",
        "url": "https://www.retrogames.cc/embed/43879-street-hoop-street-slam-dunk-dream-dem-004-deh-004.html",
        "console": "ARCADE",
        "color": "#ffd700",
        "icon": "🏀",
        "controls": [
            "**Joystick :** Déplacement joueur",
            "**Bouton 1 :** Passe/Tir normal",
            "**Bouton 2 :** Saut/Dunk",
            "**Bouton 3 :** Tir spécial",
            "**Start :** Insérer pièce/Démarrer",
            "**Select :** Choix équipe/Options",
            "**Combinaisons :** Alley-oop spécial"
        ]
    }
}

# Initialisation de l'état
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = 'streethoop'

def change_game(game_id):
    st.session_state.selected_game = game_id

# Interface principale
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="neon-title">ÉMULATEUR NÉON</h1>', unsafe_allow_html=True)

# Sélecteur de jeu avec 8 boutons (2 lignes de 4)
st.markdown('<div class="game-button-container">', unsafe_allow_html=True)

# Première ligne : 4 jeux
col1, col2, col3, col4 = st.columns(4)
game_ids = list(GAMES.keys())

# Ligne 1
with col1:
    game_id = game_ids[0]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col2:
    game_id = game_ids[1]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0]}"
    if len(game['name'].split()[0]) > 6:
        btn_label = f"{game['icon']} {game['name'].split()[0][:6]}."
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col3:
    game_id = game_ids[2]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col4:
    game_id = game_ids[3]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

st.markdown('</div>', unsafe_allow_html=True)

# Deuxième ligne : 4 autres jeux
st.markdown('<div class="game-button-container">', unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)

# Ligne 2
with col5:
    game_id = game_ids[4]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col6:
    game_id = game_ids[5]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col7:
    game_id = game_ids[6]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

with col8:
    game_id = game_ids[7]
    game = GAMES[game_id]
    is_active = st.session_state.selected_game == game_id
    btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
    if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                type="primary" if is_active else "secondary"):
        change_game(game_id)

st.markdown('</div>', unsafe_allow_html=True)

# Affichage du jeu sélectionné
game = GAMES[st.session_state.selected_game]

# Affichage du titre avec badge spécial pour Arcade
if game["console"] == "ARCADE":
    badge_class = "arcade-badge"
else:
    badge_class = "console-badge"

st.markdown(f'''
    <h2 class="game-title">
        {game["icon"]} {game["name"]}
        <span class="{badge_class}" style="border-color: {game['color']}; color: {game['color']};">
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
        height="500"
        frameborder="no"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
        title="{game['name']} - Émulateur"
        sandbox="allow-scripts allow-same-origin allow-popups">
    </iframe>
</div>
''', unsafe_allow_html=True)

# Section des commandes
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
st.markdown(f'''
<h3 style="color:{game['color']}; text-shadow: 0 0 7px {game['color']};">
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
    if st.button("💾 SAUVEGARDE", use_container_width=True, 
                help="Sauvegarde de progression"):
        if game["console"] == "ARCADE":
            st.info("Arcade : Sauvegarde des highscores via menu émulateur")
        else:
            st.info(f"Pour {game['console']} : Menu émulateur → icône disquette")

with col2:
    if st.button("🔄 REDÉMARRER", use_container_width=True, 
                help="Redémarre le jeu actuel"):
        st.rerun()

with col3:
    if st.button("🎛️ CONFIGURER", use_container_width=True, 
                help="Configuration émulateur"):
        if game["console"] == "ARCADE":
            st.info("""
            **Configuration Arcade recommandée :**
            • Contrôles : Joystick + 3 boutons
            • Difficulté : Réglable dans le jeu
            • Pièces illimitées : Option émulateur
            • Affichage : Ratio 4:3 pour aspect original
            """)
        else:
            st.info("Configurations disponibles dans le menu intégré de l'émulateur.")

st.markdown('</div>', unsafe_allow_html=True)

# Section informations spécifiques pour Street Hoop
if st.session_state.selected_game == "streethoop":
    with st.expander("🏀 **INFORMATIONS STREET HOOP**", expanded=False):
        st.markdown("""
        ### À propos du jeu :
        **Street Hoop** (aussi connu sous **Street Slam** ou **Dunk Dream**) est un jeu de basket arcade sorti en 1994 par Data East.
        
        ### Caractéristiques :
        - **Développeur** : Data East
        - **Éditeur** : Data East
        - **Sortie** : 1994
        - **Genre** : Basket arcade / Street
        - **PCB** : DEM-004 / DEH-004
        
        ### Particularités Arcade :
        • **Gameplay arcade** : Simple, rapide et addictif
        • **Graphismes** : Style cartoon années 90
        • **Joueurs** : Jusqu'à 4 joueurs (2vs2)
        • **Système de pièces** : Authentique expérience salle d'arcade
        
        ### Équipes et personnages :
        1. **Équipe USA** : Style street agressif
        2. **Équipe Europe** : Jeu technique
        3. **Équipe Japon** : Rapidité et précision
        4. **Équipe Monde** : Mix des styles
        
        ### Gameplay :
        - **Dunks spectaculaires** : Animations spéciales
        - **Alley-oops** : Combinaisons à 2 joueurs
        - **Power-ups** : Boosts temporaires
        - **Mode tournoi** : Championnat international
        
        ### Conseils pour émulation Arcade :
        • Activez les **pièces illimitées** pour pratiquer
        • Réglez la **difficulté** selon votre niveau
        • **Joystick recommandé** pour mouvements fluides
        • Expérience **2 joueurs** disponible (partage écran)
        """)

# Section informations générales
with st.expander("ℹ️ **INFORMATIONS IMPORTANTES**", expanded=False):
    st.markdown("""
    ### Instructions d'utilisation :
    1. **Cliquez sur l'iframe** pour activer les commandes
    2. **Pour Arcade** : Appuyez sur START pour insérer une pièce
    3. **Contrôles** : Adaptés à chaque type de console
    4. **Sauvegarde** : Menu émulateur → icône disquette
    
    ### Compatibilité multi-consoles :
    - **SNES/MegaDrive** : Compatibilité optimale
    - **PlayStation** : Bonne performance
    - **Nintendo 64/DS** : Chrome/Firefox recommandés
    - **Arcade** : Support MAME optimal
    
    ### Performance :
    - Les jeux Arcade sont généralement légers
    - Connexion internet stable recommandée
    - Plein écran disponible via l'émulateur
    - Son stéréo pour une expérience immersive
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer">
    <p>Émulateur fourni par RetroGames.cc | Design Néon © 2024</p>
    <p style="font-size: 0.7em; color: #00aaff;">
        🎮 8 jeux disponibles • 📺 6 types supportés • ⚡ Expérience optimisée
    </p>
</div>
''', unsafe_allow_html=True)

# Sidebar avec statistiques
with st.sidebar:
    st.markdown("### 📊 TABLEAU DE BORD")
    
    # Compteur par type de console
    console_types = {}
    for game in GAMES.values():
        console = game["console"]
        console_types[console] = console_types.get(console, 0) + 1
    
    # Métriques
    st.metric("Total des jeux", len(GAMES))
    st.metric("Types supportés", len(console_types))
    
    # Distribution par type
    st.markdown("---")
    st.markdown("### 🎯 RÉPARTITION")
    for console, count in console_types.items():
        percentage = (count / len(GAMES)) * 100
        st.write(f"**{console}** : {count} jeu{'s' if count > 1 else ''}")
        st.progress(percentage/100, text=f"{percentage:.1f}%")
    
    st.markdown("---")
    st.markdown("### 🚀 NAVIGATION RAPIDE")
    
    # Boutons de navigation avec icônes
    for game_id, game_info in GAMES.items():
        if st.button(
            f"{game_info['icon']} {game_info['name'].split()[0]}", 
            key=f"sidebar_{game_id}",
            use_container_width=True,
            type="primary" if st.session_state.selected_game == game_id else "secondary"
        ):
            change_game(game_id)
    
    st.markdown("---")
    st.markdown("### ⚙️ PARAMÈTRES ARCADE")
    
    # Paramètres spécifiques Arcade
    if st.session_state.selected_game == "streethoop":
        st.markdown("**Options Street Hoop :**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            coins = st.selectbox("Pièces", ["Illimitées", "3 par crédit", "Arcade réel"])
        
        with col_b:
            difficulty = st.select_slider(
                "Difficulté",
                options=["Très Facile", "Facile", "Normal", "Difficile", "Expert"]
            )
        
        if st.button("⚙️ Appliquer paramètres Arcade", use_container_width=True):
            st.success(f"✅ Pièces: {coins} | Difficulté: {difficulty}")
    else:
        # Paramètres généraux
        col_a, col_b = st.columns(2)
        with col_a:
            volume = st.slider("🔊", 0, 100, 80, key="volume_slider")
        
        with col_b:
            quality = st.selectbox(
                "🎨", 
                ["Haute", "Moyenne", "Basse"],
                index=0,
                key="quality_select"
            )
        
        if st.button("🔄 Appliquer paramètres", use_container_width=True):
            st.success(f"✅ Volume: {volume}% | Qualité: {quality}")

# Note de fin spéciale pour Arcade
st.markdown('''
<style>
.arcade-tip {
    text-align: center;
    margin-top: 15px;
    font-size: 0.75em;
    color: #ffd700;
    font-style: italic;
    text-shadow: 0 0 5px #ffd700;
}
</style>
<div class="arcade-tip">
    🏀 Astuce Street Hoop : Pour un alley-oop, appuyez sur BOUTON 2 près du panier avec un coéquipier libre !
</div>
''', unsafe_allow_html=True)
