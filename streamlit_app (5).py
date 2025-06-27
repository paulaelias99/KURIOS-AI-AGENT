import streamlit as st
import json
import re

# Cargar cursos base
@st.cache_data
def load_courses():
    with open("kurios_cursos.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Extraer semanas solicitadas (si el usuario dice "2 semanas", etc.)
def extraer_duracion(texto):
    match = re.search(r"(\\d+)\\s*semanas?", texto.lower())
    if match:
        return int(match.group(1))
    return None

# Buscar módulos relevantes desde múltiples cursos según el pedido
def buscar_modulos_relevantes(cursos, pedido):
    pedido = pedido.lower()
    modulos = []

    for curso in cursos:
        for semana in curso["programa"]:
            for modulo in semana["modulos"]:
                nombre = modulo["nombre"].lower()
                contenido_texto = " ".join(modulo.get("contenido", [])).lower()
                if any(palabra in nombre or palabra in contenido_texto for palabra in pedido.split()):
                    modulos.append(modulo)
    return modulos

# Generar markdown de los módulos seleccionados
def generar_markdown(modulos, semanas_max):
    md = "# Curso Personalizado\\n\\n"
    modulos_limitados = modulos[:semanas_max * 2] if semanas_max else modulos  # ~2 módulos por semana
    for i, m in enumerate(modulos_limitados, 1):
        md += f"## Módulo {i}: {m['nombre']}\\n"
        for item in m.get("contenido", []):
            md += f"- {item}\\n"
        md += "\\n"
    if semanas_max and len(modulos) > len(modulos_limitados):
        md += f"_(Se mostraron solo los primeros {len(modulos_limitados)} módulos para ajustarse a {semanas_max} semanas.)_\\n"
    return md

# Interfaz de usuario
st.title("🧠 Kurios AI Course Builder")
st.markdown("Genera un curso personalizado basado en los cursos de Kurios. Mezcla temas, limita duración y obtén una propuesta estructurada.")

user_input = st.text_area("📝 ¿Qué curso necesitas?",
    placeholder="Ej: Quiero un curso que combine Growth 101 y Monetization Strategy, solo con módulos de pricing y adquisición, y que dure 2 semanas")

if st.button("Generar Curso"):
    cursos = load_courses()
    semanas_deseadas = extraer_duracion(user_input)
    modulos_relevantes = buscar_modulos_relevantes(cursos, user_input)

    if modulos_relevantes:
        st.success("✅ Curso generado")
        markdown_resultado = generar_markdown(modulos_relevantes, semanas_deseadas)
        st.markdown(markdown_resultado)
        st.download_button("⬇️ Descargar como .md", markdown_resultado, file_name="curso_personalizado.md")
    else:
        st.warning("No se encontraron módulos que coincidan con tu pedido.)
