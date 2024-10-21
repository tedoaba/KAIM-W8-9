from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import shap

def get_models():
    models = [
        ("Logistic Regression", LogisticRegression(C=1, solver='liblinear')),
        ("Random Forest", RandomForestClassifier(n_estimators=30, max_depth=3)),
        ("XGBClassifier", XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
        ("Decision Tree", DecisionTreeClassifier(max_depth=5)),
    ]
    return models

def train_models(datasets, models):
    reports = {}
    shap_values_dict= {}

    for dataset_name, (X_train, y_train, X_test, y_test) in datasets.items():
        dataset_reports = []
        shap_values_dict[dataset_name] = {}

        for model_name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            dataset_reports.append((model_name, model, report))

            try:
                # compute SHAP values
                if model_name == "Logistic Regression":
                    explainer = shap.Explainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "Random Forest":
                    explainer = shap.TreeExplainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "Decision Tree":
                    explainer = shap.TreeExplainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "XGBClassifier":
                    explainer = shap.Explainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                else:
                    explainer = shap.KernelExplainer(model.predict, X_train)
                    shap_values = explainer.shap_values(X_test)

                shap_values_dict[dataset_name][model_name] = shap_values

                shap.summary_plot(shap_values, X_test, feature_names=X_train.columns, plot_type="bar", show=False)
                plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_summary.png')
                plt.close()
            except Exception as e:
                print(f"SHAP calculation fialed for {model_name} on {dataset_name}: {e}")

        reports[dataset_name] = dataset_reports
        shap_values_dict[dataset_name] = shap_values_dict

    return reports, shap_values_dict
