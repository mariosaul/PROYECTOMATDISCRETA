import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile

# Título de la aplicación
st.title("Visualizador Interactivo de Flujos de Información")

# Sección para ingresar los departamentos
st.header("1. Ingresar Departamentos")
departamentos = st.text_input("Escribe los nombres de los departamentos separados por comas:", "A,B,C,D,E,F")
departamentos = [dep.strip() for dep in departamentos.split(",")]

# Sección para ingresar las conexiones
st.header("2. Ingresar Conexiones y Flujo de Información")

# Crear una lista para almacenar las conexiones
if "conexiones" not in st.session_state:
    st.session_state.conexiones = []

col1, col2, col3 = st.columns(3)
with col1:
    origen = st.selectbox("Origen", ["Seleccionar"] + departamentos, key="origen")
with col2:
    destino = st.selectbox("Destino", ["Seleccionar"] + departamentos, key="destino")
with col3:
    flujo = st.number_input("Flujo de Información", min_value=1, step=1, key="flujo")

if st.button("Añadir Conexión"):
    if origen != "Seleccionar" and destino != "Seleccionar" and origen != destino:
        st.session_state.conexiones.append((origen, destino, flujo))
    else:
        st.warning("Por favor selecciona un origen y un destino válidos.")

# Mostrar las conexiones actuales
if st.session_state.conexiones:
    st.subheader("Conexiones Actuales")
    st.table(st.session_state.conexiones)

# Función para ejecutar el algoritmo de Dijkstra
def dijkstra(G, origen, destino):
    distancias, caminos = nx.single_source_dijkstra(G, origen, weight='weight')

    if destino in caminos:
        camino = caminos[destino]
        flujo_total = distancias[destino]
        return camino, flujo_total
    else:
        return None, float('inf')  # Si no hay camino, retornar infinito

# Sección para ejecutar Dijkstra
st.header("3. Ejecutar Algoritmo de Dijkstra")

# Seleccionar el origen y destino para Dijkstra
origen_dijkstra = st.selectbox("Seleccionar Nodo de Origen para Dijkstra", departamentos)
destino_dijkstra = st.selectbox("Seleccionar Nodo de Destino para Dijkstra", departamentos)

# Variables para mostrar el camino más corto
camino_mostrado = None
flujo_total_mostrado = None

if st.button("Ejecutar Dijkstra"):
    if origen_dijkstra != destino_dijkstra:
        # Crear el grafo con las conexiones actuales
        G = nx.DiGraph()
        G.add_nodes_from(departamentos)
        G.add_weighted_edges_from(st.session_state.conexiones)

        # Ejecutar el algoritmo de Dijkstra
        camino, flujo_total = dijkstra(G, origen_dijkstra, destino_dijkstra)
        if camino:
            camino_mostrado = camino
            flujo_total_mostrado = flujo_total
            st.write(f"El camino más corto desde {origen_dijkstra} a {destino_dijkstra} es {camino} con un flujo total de {flujo_total}")
        else:
            st.write(f"No hay un camino válido entre {origen_dijkstra} y {destino_dijkstra}")

# Visualización con PyVis
st.header("4. Visualización Interactiva del Grafo")
if st.session_state.conexiones:
    # Crear un grafo dirigido
    G = nx.DiGraph()
    G.add_nodes_from(departamentos)
    G.add_weighted_edges_from(st.session_state.conexiones)

    # Crear la visualización con PyVis
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)

    # Personalizar la visualización de los nodos
    for node in G.nodes:
        net.get_node(node)["label"] = node

    # Mostrar el costo (peso) de cada arista
    for u, v, data in G.edges(data=True):
        weight = data.get('weight')  # Usamos .get() para evitar KeyError
        if weight is not None:
            net.add_edge(u, v, title=str(weight), value=weight)  # title será el peso visible

    # Resaltar el camino más corto si se ejecutó Dijkstra
    if camino_mostrado:
        for i in range(len(camino_mostrado) - 1):
            net.get_edge(camino_mostrado[i], camino_mostrado[i + 1])['color'] = 'red'
            net.get_edge(camino_mostrado[i], camino_mostrado[i + 1])['width'] = 3

    # Guardar en un archivo temporal y mostrarlo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        st.components.v1.html(open(tmp_file.name).read(), height=600)

# Mostrar el camino calculado sin quitar el grafo
if camino_mostrado:
    st.subheader("Camino Calculado por Dijkstra")
    st.write(f"El camino más corto desde {origen_dijkstra} a {destino_dijkstra} es {camino_mostrado} con un flujo total de {flujo_total_mostrado}")






