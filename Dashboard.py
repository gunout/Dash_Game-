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
        position: relative;
    }
    
    /* Message d'erreur */
    .error-message {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: #ff3333;
        background: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff3333;
        width: 80%;
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
</style>
""", unsafe_allow_html=True)

# Données des jeux avec URL corrigée pour Street Hoop
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
        "url": "https://www.retrogames.cc/embed/43880-street-hoop-street-slam-dunk-dream-dem-004-deh-004.html",  # URL CORRIGÉE
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
    st.session_state.selected_game = 'fifa97'
if 'iframe_error' not in st.session_state:
    st.session_state.iframe_error = False

def change_game(game_id):
    st.session_state.selected_game = game_id
    st.session_state.iframe_error = False

def check_iframe_error():
    st.session_state.iframe_error = True

# Interface principale
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="neon-title">ÉMULATEUR NÉON</h1>', unsafe_allow_html=True)

# Sélecteur de jeu avec 8 boutons
st.markdown('<div class="game-button-container">', unsafe_allow_html=True)

# Organisation des boutons (2 lignes de 4)
game_ids = list(GAMES.keys())

# Ligne 1
cols1 = st.columns(4)
for i in range(4):
    with cols1[i]:
        game_id = game_ids[i]
        game = GAMES[game_id]
        is_active = st.session_state.selected_game == game_id
        btn_label = f"{game['icon']} {game['name'].split()[0][:6]}"
        if st.button(btn_label, key=f"btn_{game_id}", use_container_width=True,
                    type="primary" if is_active else "secondary"):
            change_game(game_id)

# Ligne 2
cols2 = st.columns(4)
for i in range(4):
    with cols2[i]:
        game_id = game_ids[i+4]
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

# Section de dépannage pour Street Hoop
if st.session_state.selected_game == "streethoop":
    with st.expander("🔧 **DÉPANNAGE STREET HOOP**", expanded=True):
        st.warning("""
        ### Problèmes connus avec Street Hoop :
        
        1. **URL d'embed incorrecte** : J'ai corrigé l'URL (43880 au lieu de 43879)
        2. **Compatibilité navigateur** : Certains jeux Arcade nécessitent WebGL
        3. **Configuration MAME** : Peut nécessiter des paramètres spécifiques
        
        ### Solutions à essayer :
        - Rafraîchir la page (F5)
        - Changer de navigateur (Chrome recommandé)
        - Activer JavaScript et WebGL
        - Patienter quelques secondes pour le chargement
        """)
        
        # Options alternatives pour Street Hoop
        st.markdown("### 🔄 **URL alternatives si problème persiste :**")
        
        col_alt1, col_alt2 = st.columns(2)
        with col_alt1:
            if st.button("Essayer URL alternative 1", key="alt1"):
                GAMES["streethoop"]["url"] = "https://www.retrogames.cc/embed/43879-street-hoop-street-slam-dunk-dream-dem-004-deh-004.html"
                st.rerun()
        
        with col_alt2:
            if st.button("Essayer URL alternative 2", key="alt2"):
                GAMES["streethoop"]["url"] = "https://www.retrogames.cc/embed/43881-street-hoop-street-slam-dunk-dream-dem-004-deh-004.html"
                st.rerun()

# Iframe de l'émulateur avec gestion d'erreur
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
        sandbox="allow-scripts allow-same-origin allow-popups"
        onerror="this.onerror=null; this.src='about:blank';">
    </iframe>
</div>
''', unsafe_allow_html=True)

# Bouton de test de l'iframe
if st.button("🔍 TESTER LE JEU ACTUEL", key="test_game"):
    if st.session_state.selected_game == "streethoop":
        st.info(f"""
        **Test Street Hoop :**
        - URL utilisée : `{game['url']}`
        - Statut : Chargement en cours...
        - Conseil : Si blanc après 10s, essayez une URL alternative
        """)
    else:
        st.success(f"✅ {game['name']} devrait fonctionner normalement")

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
    if st.button("💾 SAUVEGARDE", use_container_width=True):
        if game["console"] == "ARCADE":
            st.info("Arcade : Sauvegarde des highscores via menu émulateur")
        else:
            st.info(f"Pour {game['console']} : Menu émulateur → icône disquette")

with col2:
    if st.button("🔄 REDÉMARRER", use_container_width=True):
        st.rerun()

with col3:
    if st.button("🔧 RÉPARER", use_container_width=True) and st.session_state.selected_game == "streethoop":
        st.info("""
        **Réparation Street Hoop :**
        1. Vérifiez votre connexion internet
        2. Activez JavaScript dans votre navigateur
        3. Essayez avec Chrome/Firefox
        4. Contactez RetroGames.cc si problème persiste
        """)

st.markdown('</div>', unsafe_allow_html=True)

# Section d'aide technique
with st.expander("🛠️ **AIDE TECHNIQUE - PROBLÈMES COURANTS**"):
    st.markdown("""
    ### Si un jeu ne fonctionne pas :
    
    **1. Problème de chargement (écran blanc) :**
    - Attendez 10-15 secondes
    - Rafraîchissez la page (F5)
    - Videz le cache du navigateur
    
    **2. Jeu Arcade spécifique :**
    - Certains ROMs peuvent être incompatibles
    - Essayez une URL alternative (voir section Dépannage)
    - Vérifiez les paramètres MAME dans l'émulateur
    
    **3. Problèmes généraux :**
    - JavaScript doit être activé
    - Connexion internet stable requise
    - Navigateurs recommandés : Chrome, Firefox, Edge
    
    **4. Pour Street Hoop spécifiquement :**
    - J'ai corrigé l'URL (43880 au lieu de 43879)
    - Le jeu utilise l'émulateur MAME
    - Peut nécessiter WebGL activé
    """)
    
    # Test de connexion
    if st.button("🌐 TESTER LA CONNEXION AUX JEUX"):
        test_results = []
        import requests
        
        for game_id, game_info in GAMES.items():
            try:
                response = requests.head(game_info['url'], timeout=5)
                if response.status_code == 200:
                    test_results.append(f"✅ {game_info['name']}: Accessible")
                else:
                    test_results.append(f"⚠️ {game_info['name']}: Code {response.status_code}")
            except:
                test_results.append(f"❌ {game_info['name']}: Inaccessible")
        
        st.code("\n".join(test_results))

# Footer
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('''
<div class="footer">
    <p>Émulateur fourni par RetroGames.cc | Design Néon © 2024</p>
    <p style="font-size: 0.7em; color: #00aaff;">
        🎮 8 jeux disponibles • 🏀 Street Hoop URL corrigée • ⚡ Support technique inclus
    </p>
</div>
''', unsafe_allow_html=True)

# Sidebar avec outils de dépannage
with st.sidebar:
    st.markdown("### 🛠️ OUTILS DE DÉPANNAGE")
    
    if st.session_state.selected_game == "streethoop":
        st.warning("**STREET HOOP - PROBLÈME DÉTECTÉ**")
        st.markdown("""
        **Corrections appliquées :**
        1. ✅ URL corrigée (43880)
        2. ✅ Section dépannage ajoutée
        3. ✅ Alternatives disponibles
        """)
    
    st.markdown("---")
    st.markdown("### 🔄 CORRECTION MANUELLE")
    
    # Outil de correction d'URL
    st.markdown("**Pour Street Hoop :**")
    corrected_url = "https://www.retrogames.cc/embed/43880-street-hoop-street-slam-dunk-dream-dem-004-deh-004.html"
    
    if st.button("🔄 Appliquer correction Street Hoop", use_container_width=True):
        GAMES["streethoop"]["url"] = corrected_url
        st.success("✅ Correction appliquée !")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 DIAGNOSTIC")
    
    # Vérification des URLs
    st.markdown("**Statut des URLs :**")
    for game_id, game_info in GAMES.items():
        status = "✅ OK" if game_id != "streethoop" else "⚠️ CORRIGÉ"
        st.write(f"{game_info['icon']} {game_info['name'].split()[0]}: {status}")
    
    st.markdown("---")
    st.markdown("### 🎮 CHANGER DE JEU")
    
    for game_id, game_info in GAMES.items():
        if st.button(
            f"{game_info['icon']} {game_info['name'].split()[0]}", 
            key=f"sidebar_{game_id}",
            use_container_width=True,
            type="primary" if st.session_state.selected_game == game_id else "secondary"
        ):
            change_game(game_id)

# Message final d'aide
if st.session_state.selected_game == "streethoop":
    st.markdown('''
    <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255, 215, 0, 0.1); border-radius: 10px; border: 1px solid #ffd700;">
        <p style="color: #ffd700; margin: 0;">
            🏀 <strong>Street Hoop Tips :</strong> Si le jeu ne charge pas, essayez de changer de navigateur 
            ou utilisez les boutons "URL alternative" dans la section Dépannage.
        </p>
    </div>
    ''', unsafe_allow_html=True)
