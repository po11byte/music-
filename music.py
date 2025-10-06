import streamlit as st
import requests

st.set_page_config(page_title="Music Explorer", layout="centered")
st.title("🎵 Music Explorer")
st.write("Busca información sobre artistas y canciones usando Last.fm API")


API_KEY = "3b1c697b680f2aff22367d562508bff4" 

def buscar_musica(tipo, query):
    """Buscar música en Last.fm API"""
    url = "http://ws.audioscrobbler.com/2.0/"
    
    params = {
        'method': f'{tipo}.search',
        f'{tipo}': query,
        'api_key': API_KEY,
        'format': 'json',
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def mostrar_imagen_segura(imagen_data, width=100):
    """Muestra imágenes de manera segura, manejando URLs vacías"""
    if (imagen_data and len(imagen_data) > 2 and 
        imagen_data[2]["#text"] and 
        imagen_data[2]["#text"].startswith('http')):
        try:
            st.image(imagen_data[2]["#text"], width=width)
        except:
            st.image("https://via.placeholder.com/100x100/333333/FFFFFF?text=🎵", width=width)
    else:
        st.image("https://via.placeholder.com/100x100/333333/FFFFFF?text=🎵", width=width)


with st.sidebar:
    st.header("⚙️ Configuración")
    tipo_busqueda = st.selectbox(
        "Tipo de búsqueda:",
        ["Artistas", "Canciones", "Álbumes"]
    )
    
    if tipo_busqueda == "Artistas":
        metodo = "artist"
    elif tipo_busqueda == "Canciones":
        metodo = "track"
    else:
        metodo = "album"


busqueda = st.text_input("🔍 Escribe el nombre del artista, canción o álbum:")

col1, col2 = st.columns([1, 1])
with col1:
    buscar_btn = st.button("🎵 Buscar Música", use_container_width=True)
with col2:
    if st.button("🧹 Limpiar", use_container_width=True):
        st.rerun()

if buscar_btn:
    if not API_KEY or API_KEY == "a3df7d1c2f8a4b5e6c7d8e9f0a1b2c3d":
        st.error(" **Configura tu API Key de Last.fm**")
        st.info("""
        **📝 Cómo obtener tu API Key:**
        
        1. 🌐 **Ve a:** https://www.last.fm/api
        2. 👤 **Inicia sesión o regístrate** (gratis)
        3. 🔑 **Haz clic en:** "Get an API account"
        4. 📝 **Llena el formulario:**
           - App name: "Music Explorer"
           - Description: "App personal de música"
           - Organization: "Personal"
        5.  **Copia tu API Key** y pégala en el código
        """)
        
    elif not busqueda:
        st.warning(" Por favor, escribe algo para buscar")
        
    else:
        with st.spinner(f"🔍 Buscando {tipo_busqueda.lower()}..."):
            resultados = buscar_musica(metodo, busqueda)
            
            if resultados:
                
                if metodo == "artist":
                    artists = resultados.get("results", {}).get("artistmatches", {}).get("artist", [])
                    if artists:
                        st.success(f" Encontrados {len(artists)} artistas para: '{busqueda}'")
                        for artist in artists:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_segura(artist.get("image"), width=100)
                                with col2:
                                    st.subheader(artist["name"])
                                    if artist.get("listeners"):
                                        st.write(f" **Oyentes:** {artist['listeners']}")
                                    if artist.get("url"):
                                        st.markdown(f"[ Ver perfil]({artist['url']})")
                                st.markdown("---")
                    else:
                        st.warning(f" No se encontraron artistas para: '{busqueda}'")
                
                
                elif metodo == "track":
                    tracks = resultados.get("results", {}).get("trackmatches", {}).get("track", [])
                    if tracks:
                        st.success(f" Encontradas {len(tracks)} canciones para: '{busqueda}'")
                        for track in tracks:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_segura(track.get("image"), width=100)
                                with col2:
                                    st.subheader(track["name"])
                                    st.write(f" **Artista:** {track.get('artist', 'N/A')}")
                                    if track.get("url"):
                                        st.markdown(f"[ Escuchar preview]({track['url']})")
                                st.markdown("---")
                    else:
                        st.warning(f" No se encontraron canciones para: '{busqueda}'")
                
               
                elif metodo == "album":
                    albums = resultados.get("results", {}).get("albummatches", {}).get("album", [])
                    if albums:
                        st.success(f" Encontrados {len(albums)} álbumes para: '{busqueda}'")
                        for album in albums:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_segura(album.get("image"), width=100)
                                with col2:
                                    st.subheader(album["name"])
                                    st.write(f" **Artista:** {album.get('artist', 'N/A')}")
                                    if album.get("url"):
                                        st.markdown(f"[ Ver álbum]({album['url']})")
                                st.markdown("---")
                    else:
                        st.warning(f" No se encontraron álbumes para: '{busqueda}'")
            else:
                st.error("Error al conectar con Last.fm API")


st.markdown("---")
st.caption(" Conectado a Last.fm API | Creado con Streamlit")

if not API_KEY or API_KEY == "3b1c697b680f2aff22367d562508bff4":
    st.sidebar.warning(" **Configura tu API Key**")
    st.sidebar.info("Una vez que tengas tu API Key de Last.fm, reemplázala en la línea 8 del código.")
