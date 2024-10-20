import mlflow
import mlflow.sklearn
import mlflow.xgboost
import mlflow.keras
from sklearn.metrics import classification_report

def evaluate_models(models, datasets):
    """Train and evaluate models on each dataset."""
    for dataset_name, (X_train, y_train, X_test, y_test) in datasets.items():
        reports = []

        for model_name, model in models:
            print(f"Training {model_name} on {dataset_name}")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            reports.append(report)

        log_to_mlflow(models, reports, dataset_name)


def log_to_mlflow(models, reports, dataset_name):
    """Log model performance metrics and models to MLflow."""
    mlflow.set_experiment("Fraud Detection Models - 2 Datasets")
    mlflow.set_tracking_uri("http://localhost:5000")

    for i, (model_name, model) in enumerate(models):
        report = reports[i]

        with mlflow.start_run(run_name=f"{model_name}_{dataset_name}"):
            mlflow.log_param("model", model_name)
            mlflow.log_param("dataset", dataset_name)
            mlflow.log_metric('accuracy', report['accuracy'])
            mlflow.log_metric('recall_class_1', report['1']['recall'])
            mlflow.log_metric('recall_class_0', report['0']['recall'])
            mlflow.log_metric('f1_score_macro', report['macro avg']['f1-score'])

            # Log model to MLflow
            if "XGB" in model_name:
                mlflow.xgboost.log_model(model, "model")
            elif "CNN" in model_name or "RNN" in model_name or "LSTM" in model_name:
                mlflow.keras.log_model(model, "model")
            else:
                mlflow.sklearn.log_model(model, "model")
