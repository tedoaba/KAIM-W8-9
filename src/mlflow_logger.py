import mlflow
import mlflow.sklearn
import mlflow.xgboost
import os

def initialize_mlflow(experiment_name, tracking_uri):
    # Set the tracking URI for MLflow
    mlflow.set_tracking_uri(tracking_uri)

    # Check if the experiment exists
    try:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            print(f"Creating experiment: {experiment_name}")
            mlflow.create_experiment(experiment_name)
        else:
            print(f"Using existing experiment: {experiment_name}")
        mlflow.set_experiment(experiment_name)
    except Exception as e:
        print(f"Error initializing MLflow experiment: {e}")

def log_model_performance_to_mlflow(reports, shap_values_dict, lime_explanations):
    for dataset_name, model_reports in reports.items():
        for model_name, model, report in model_reports:
            with mlflow.start_run(run_name=f"{model_name}_{dataset_name}"):
                mlflow.log_param("model", model_name)
                mlflow.log_param("dataset", dataset_name)
                mlflow.log_metric('accuracy', report['accuracy'])
                mlflow.log_metric('recall_class_1', report['1']['recall'])
                mlflow.log_metric('recall_class_0', report['0']['recall'])
                mlflow.log_metric('f1_score_macro', report['macro avg']['f1-score'])

                # Log the model
                if "XGBClassifier" in model_name:
                    mlflow.xgboost.log_model(model, "model")
                else:
                    mlflow.sklearn.log_model(model, "model")

                
                # SHAP
                shap_plot_path = f"../plots/{dataset_name}_{model_name}_shap_summary.png"
                lime_explanations_path = f'../lime_explanations/{dataset_name}_{model_name}_lime.html'
                if os.path.exists(shap_plot_path):
                    mlflow.log_artifact(shap_plot_path)
                if os.path.exists(lime_explanations_path):
                    mlflow.log_artifact(lime_explanations_path)
