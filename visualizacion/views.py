import pandas as pd
import arff
from django.shortcuts import render
from pathlib import Path

def mostrar_datos(request):
    # Ruta al archivo ARFF reducido
    ruta = Path(__file__).resolve().parent.parent / "datasets" / "datasets" / "NSL-KDD" / "KDDTrain_reducido.arff"

    # Verificar si el archivo existe
    if not ruta.exists():
        return render(request, "visualizacion/index.html", {
            "error": f"Archivo no encontrado: {ruta}"
        })

    # Cargar ARFF
    with open(ruta, "r") as archivo:
        data = arff.load(archivo)

    # Columnas
    columnas = [attr[0] for attr in data["attributes"]]

    # Crear DataFrame
    df = pd.DataFrame(data["data"], columns=columnas)

    # Agregar índice como primera columna
    df.reset_index(inplace=True)
    df.rename(columns={"index": "ID"}, inplace=True)

    # Actualizar columnas y registros
    columnas = df.columns.tolist()
    registros = df.head(1000).values.tolist()  

    # Renderizar template
    return render(request, "visualizacion/index.html", {
        "columnas": columnas,
        "registros": registros
    })
