import streamlit as st
import pandas as pd
import os
from zipfile import ZipFile
import shutil

# ----------------------------------------
# Inicialización de carpetas y funciones
# ----------------------------------------

def inicializar_carpetas():
    tipos = ["Alumbrado", "Envolvente", "Ventana", "Equipos_de_Clima", "Equipos_de_Aire", "Motor_Bomba", "Caldera"]
    for tipo in tipos:
        os.makedirs(f"Fotos_{tipo}", exist_ok=True)

def guardar_datos(tipo, datos):
    nombre_archivo = f"{tipo}.xlsx"
    if os.path.exists(nombre_archivo):
        df_existente = pd.read_excel(nombre_archivo)
        df_nuevo = pd.concat([df_existente, pd.DataFrame([datos])], ignore_index=True)
    else:
        df_nuevo = pd.DataFrame([datos])
    df_nuevo.to_excel(nombre_archivo, index=False)

def crear_zip():
    with ZipFile("datos_visita.zip", "w") as zipf:
        # Añadir Excels
        for archivo in os.listdir():
            if archivo.endswith(".xlsx"):
                zipf.write(archivo)
        # Añadir carpetas de fotos
        carpetas = [d for d in os.listdir() if os.path.isdir(d) and d.startswith("Fotos_")]
        for carpeta in carpetas:
            for root, _, files in os.walk(carpeta):
                for file in files:
                    zipf.write(os.path.join(root, file))

# Inicializamos carpetas
inicializar_carpetas()

# ----------------------------------------
# INTERFAZ Streamlit
# ----------------------------------------

st.title("🏢 Registro de Visita de Certificación/Auditoría Energética")

tipo_elemento = st.selectbox(
    "Selecciona el tipo de elemento que quieres registrar:",
    ["", "Alumbrado", "Envolvente", "Ventana", "Equipos de Clima", "Equipos de Aire", "Motor/Bomba", "Caldera"]
)

if st.button("Introducir datos"):
    if tipo_elemento == "":
        st.warning("¡Selecciona un tipo de elemento antes de continuar!")
    else:
        st.session_state["tipo_elemento"] = tipo_elemento
        st.rerun()

if "tipo_elemento" in st.session_state:
    tipo = st.session_state["tipo_elemento"]
    st.header(f"Formulario de registro: {tipo}")

    # ---- FORMULARIOS ----
    with st.form(key=f"formulario_{tipo}"):
        proyecto = st.text_input("Proyecto")
        tecnico = st.text_input("Técnico")
        
        if tipo == "Alumbrado":
            dependencia = st.text_input("Dependencia")
            descripcion = st.text_area("Descripción")
            num_luminarias = st.number_input("Número de luminarias", min_value=0, step=1)
            num_lamparas = st.number_input("Número de lámparas por luminaria", min_value=0, step=1)
            tecnologia = st.text_input("Tecnología de lámpara")
            modelo = st.text_input("Modelo de lámpara")
            fotografia = st.file_uploader("Fotografía", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Dependencia": dependencia, "Descripción": descripcion,
                "Número luminarias": num_luminarias, "Número lámparas por luminaria": num_lamparas,
                "Tecnología lámpara": tecnologia, "Modelo lámpara": modelo, "Fotografía": ""
            }

        elif tipo == "Envolvente":
            espacio = st.text_input("Espacio")
            tipologia = st.text_input("Tipología")
            orientacion = st.selectbox("Orientación", ["Norte", "Sur", "Este", "Oeste", "NE", "NO", "SE", "SO"])
            altura = st.number_input("Altura (m)", min_value=0.0)
            ancho = st.number_input("Ancho (m)", min_value=0.0)
            estado = st.text_input("Estado")
            comentario = st.text_area("Comentario")
            fotografia = st.file_uploader("Fotografía", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Espacio": espacio, "Tipología": tipologia,
                "Orientación": orientacion, "Altura": altura, "Ancho": ancho, "Estado": estado,
                "Comentario": comentario, "Fotografía": ""
            }

        elif tipo == "Ventana":
            espacio = st.text_input("Espacio")
            marco = st.text_input("Marco")
            vidrio = st.text_input("Vidrio")
            orientacion = st.selectbox("Orientación", ["Norte", "Sur", "Este", "Oeste", "NE", "NO", "SE", "SO"])
            altura = st.number_input("Altura (m)", min_value=0.0)
            ancho = st.number_input("Ancho (m)", min_value=0.0)
            estado = st.text_input("Estado")
            comentario = st.text_area("Comentario")
            fotografia = st.file_uploader("Fotografía", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Espacio": espacio, "Marco": marco, "Vidrio": vidrio,
                "Orientación": orientacion, "Altura": altura, "Ancho": ancho, "Estado": estado,
                "Comentario": comentario, "Fotografía": ""
            }

        elif tipo == "Equipos de Clima":
            espacio = st.text_input("Espacio Servicio")
            refrigerante = st.text_input("Refrigerante")
            capacidad_calorifica = st.number_input("Capacidad Calorífica (kW)", min_value=0.0)
            consumo_calor = st.number_input("Consumo Calor (kW)", min_value=0.0)
            cop = st.number_input("COP", min_value=0.0)
            capacidad_frigorifica = st.number_input("Capacidad Frigorífica (kW)", min_value=0.0)
            consumo_frio = st.number_input("Consumo Frío (kW)", min_value=0.0)
            eer = st.number_input("EER", min_value=0.0)
            ano = st.number_input("Año", min_value=1900, max_value=2100, step=1)
            estado = st.text_input("Estado")
            comentario = st.text_area("Comentario")
            fotografia = st.file_uploader("Fotografía", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Espacio Servicio": espacio, "Refrigerante": refrigerante,
                "Capacidad Calorífica": capacidad_calorifica, "Consumo Calor": consumo_calor, "COP": cop,
                "Capacidad Frigorífica": capacidad_frigorifica, "Consumo Frío": consumo_frio, "EER": eer,
                "Año": ano, "Estado": estado, "Comentario": comentario, "Fotografía": ""
            }

        elif tipo == "Equipos de Aire":
            modelo = st.text_input("Modelo")
            cantidad = st.number_input("Cantidad", min_value=0, step=1)
            potencia_ventilador = st.number_input("Potencia Ventilador (kW)", min_value=0.0)
            bateria_calor = st.number_input("Batería de calor (kW)", min_value=0.0)
            bateria_frio = st.number_input("Batería de frío (kW)", min_value=0.0)
            caudal = st.number_input("Caudal (m³/h)", min_value=0.0)
            espacio = st.text_input("Espacio Servicio")
            placa = st.file_uploader("Foto de la Placa", type=["jpg", "png", "jpeg"])
            fotografia = st.file_uploader("Fotografía general", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Modelo": modelo, "Cantidad": cantidad,
                "Potencia Ventilador": potencia_ventilador, "Batería Calor": bateria_calor,
                "Batería Frío": bateria_frio, "Caudal": caudal, "Espacio Servicio": espacio,
                "Foto Placa": "", "Fotografía": ""
            }

        elif tipo == "Motor/Bomba":
            funcion = st.text_input("Función")
            potencia = st.number_input("Potencia (kW)", min_value=0.0)
            eficiencia = st.number_input("Eficiencia (%)", min_value=0.0, max_value=100.0)
            variador = st.selectbox("Variador", ["Sí", "No"])
            espacio = st.text_input("Espacio")
            ano = st.number_input("Año", min_value=1900, max_value=2100, step=1)
            placa = st.file_uploader("Foto de la Placa", type=["jpg", "png", "jpeg"])
            fotografia = st.file_uploader("Fotografía general", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Función": funcion, "Potencia": potencia,
                "Eficiencia": eficiencia, "Variador": variador, "Espacio": espacio, "Año": ano,
                "Foto Placa": "", "Fotografía": ""
            }

        elif tipo == "Caldera":
            uso = st.text_input("Uso")
            combustible = st.text_input("Combustible")
            potencia = st.number_input("Potencia (kW)", min_value=0.0)
            rendimiento = st.number_input("Rendimiento (%)", min_value=0.0, max_value=100.0)
            ano = st.number_input("Año", min_value=1900, max_value=2100, step=1)
            estado = st.text_input("Estado")
            comentario = st.text_area("Comentario")
            placa = st.file_uploader("Foto de la Placa", type=["jpg", "png", "jpeg"])
            fotografia = st.file_uploader("Fotografía general", type=["jpg", "png", "jpeg"])

            datos = {
                "Proyecto": proyecto, "Técnico": tecnico, "Uso": uso, "Combustible": combustible,
                "Potencia": potencia, "Rendimiento": rendimiento, "Año": ano, "Estado": estado,
                "Comentario": comentario, "Foto Placa": "", "Fotografía": ""
            }

        submit = st.form_submit_button("Guardar Datos")

        if submit:
            # Guardar fotografías si existen
            carpeta_fotos = f"Fotos_{tipo.replace(' ', '_')}"
            if fotografia:
                nombre_foto = f"{carpeta_fotos}/{proyecto}_{tecnico}_foto.jpg"
                with open(nombre_foto, "wb") as f:
                    f.write(fotografia.getbuffer())
                datos["Fotografía"] = nombre_foto
            if "placa" in locals() and placa:
                nombre_placa = f"{carpeta_fotos}/{proyecto}_{tecnico}_placa.jpg"
                with open(nombre_placa, "wb") as f:
                    f.write(placa.getbuffer())
                datos["Foto Placa"] = nombre_placa

            guardar_datos(tipo.replace(" ", "_"), datos)
            st.success("✅ Datos guardados correctamente.")
            del st.session_state["tipo_elemento"]
            st.rerun()

# ----------------------------------------
# BOTÓN FINAL: Descargar ZIP
# ----------------------------------------

st.markdown("---")
if st.button("📥 Descargar todos los datos en ZIP"):
    crear_zip()
    with open("datos_visita.zip", "rb") as f:
        st.download_button("Descargar ZIP", f, file_name="datos_visita.zip")
# ----------------------------------------
# BOTÓN FINAL: Eliminar datos guardados
# ----------------------------------------

st.markdown("---")

# Estado para controlar confirmaciones
if "confirmar_borrado" not in st.session_state:
    st.session_state.confirmar_borrado = False

# Primer botón
if not st.session_state.confirmar_borrado:
    if st.button("🗑️ Eliminar todos los datos registrados"):
        st.session_state.confirmar_borrado = True

# Segundo botón de confirmación
if st.session_state.confirmar_borrado:
    st.warning("⚠️ ¿Estás absolutamente seguro de que quieres eliminar TODOS los datos? Esta acción no se puede deshacer.")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Sí, eliminar todo"):
            # Borrar Excels
            for archivo in os.listdir():
                if archivo.endswith(".xlsx"):
                    os.remove(archivo)
            # Borrar carpetas de fotos
            carpetas = [d for d in os.listdir() if os.path.isdir(d) and d.startswith("Fotos_")]
            for carpeta in carpetas:
                shutil.rmtree(carpeta)
            # Volver a crear carpetas vacías
            inicializar_carpetas()
            
            st.success("✅ Todos los datos y fotos han sido eliminados correctamente.")
            st.session_state.confirmar_borrado = False  # Reseteamos confirmación

    with col2:
        if st.button("❌ No, cancelar"):
            st.session_state.confirmar_borrado = False  # Cancelamos la operación

