
import streamlit as st
import json

# Cargar cursos base
@st.cache_data
def load_courses():
    with open("kurios_cursos.json", "r", encoding="utf-8") as f:
        return json.load(f)

def filtrar_modulos(cursos, pedido):
    pedido = pedido.lower()
    modulos_filtrados = []
    for curso in cursos:
        if any(nombre.lower() in pedido for nombre in curso["nombre"].lower().split()):
            for semana in curso["programa"]:
                for modulo in semana["modulos"]:
                    if any(palabra in modulo["nombre"].lower() for palabra in pedido.split()):
                        modulos_filtrados.append(modulo)
    return modulos_filtrados

def generar_markdown(modulos):
    md = "# Curso Personalizado

"
    for i, m in enumerate(modulos, 1):
        md += f"## Módulo {i}: {m['nombre']}
"
        for item in m.get("contenido", []):
            md += f"- {item}
"
        md += "\n"
    return md

# Interfaz Streamlit
st.title("🧠 Kurios AI Course Builder")
st.markdown("Genera un curso personalizado basado en los cursos de Kurios. Escribe tu pedido y deja que el agente lo arme por ti.")

user_input = st.text_area("📝 ¿Qué curso necesitas?", placeholder="Ej: Quiero un curso que combine Growth 101 y Monetization Strategy, solo con módulos de pricing y adquisición")

if st.button("Generar Curso"):
    cursos = load_courses()
    modulos = filtrar_modulos(cursos, user_input)
    if modulos:
        st.success("✅ Curso generado")
        st.markdown(generar_markdown(modulos))
    else:
        st.warning("No se encontraron módulos que coincidan con tu pedido. Intenta ser más específico.")
