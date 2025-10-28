from django.shortcuts import render
import pandas as pd
import arff
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

def mostrar_datos(request):
    table_html = None
    accuracy = None
    error = None

    if request.method == "POST" and request.FILES.get("arff_file"):
        uploaded_file = request.FILES["arff_file"]
        filename = uploaded_file.name

        # Validar extensión
        if not filename.lower().endswith(".arff"):
            error = "Error: Solo se permiten archivos con extensión .arff"
        else:
            try:
                # Leer archivo ARFF desde bytes
                arff_data = arff.load(io.StringIO(uploaded_file.read().decode("utf-8")))
                df = pd.DataFrame(arff_data['data'], columns=[attr[0] for attr in arff_data['attributes']])

                # Generar tabla HTML con índice
                table_html = df.to_html(classes="table table-striped", index=True)

                # ------------------------------
                # Calcular accuracy realista con cross-validation
                # ------------------------------
                if df.shape[1] >= 2:
                    X = df.iloc[:, :-1]
                    y = df.iloc[:, -1]

                    try:
                        # Convertir categóricas en numéricas
                        X_processed = pd.get_dummies(X)
                        y_processed = pd.factorize(y)[0]

                        # Modelo RandomForest
                        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)

                        # Cross-validation 5-fold
                        scores = cross_val_score(model, X_processed, y_processed, cv=5)
                        accuracy = f"{scores.mean()*100:.2f}%"

                    except Exception as e:
                        accuracy = f"No se pudo calcular accuracy: {str(e)}"

            except Exception as e:
                error = f"Error al leer el archivo: {str(e)}"

    return render(request, "visualizacion/index.html", {
        "table": table_html,
        "accuracy": accuracy,
        "error": error
    })
