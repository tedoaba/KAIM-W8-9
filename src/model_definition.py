from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular

def get_models():
    models = [
        ("Logistic_Regression", LogisticRegression(C=1, solver='liblinear')),
        ("Random_Forest", RandomForestClassifier(n_estimators=30, max_depth=3)),
        ("XGBClassifier", XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
        ("Decision_Tree", DecisionTreeClassifier(max_depth=5)),
    ]
    return models

def train_models(datasets, models):
    reports = {}
    shap_values_dict= {}
    lime_explanations = {}

    for dataset_name, (X_train, y_train, X_test, y_test) in datasets.items():
        dataset_reports = []
        shap_values_dict[dataset_name] = {}
        lime_explanations[dataset_name] = {}

        # LIME
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names = X_train.columns,
            class_names=['Class 0', 'Class 1'],
            discretize_continuous=True
        )

        for model_name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            dataset_reports.append((model_name, model, report))

            try:
                # compute SHAP values
                if model_name == "Logistic_Regression":
                    explainer = shap.Explainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "Random_Forest":
                    explainer = shap.TreeExplainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "Decision_Tree":
                    explainer = shap.TreeExplainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                elif model_name == "XGBClassifier":
                    explainer = shap.Explainer(model, X_train)
                    shap_values = explainer.shap_values(X_test)
                else:
                    explainer = shap.KernelExplainer(model.predict, X_train)
                    shap_values = explainer.shap_values(X_test)

                shap_values_dict[dataset_name][model_name] = shap_values

                if model_name == "Random_Forest":
                    # SHAP Summary Plot
                    shap.summary_plot(shap_values, X_test, feature_names=X_train.columns, plot_type="bar", show=False)
                    plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_summary.png')
                    plt.close()

                    # SHAP Dependence Plot for the first feature
                    shap.dependence_plot(0, shap_values[1], X_test, feature_names=X_train.columns, show=False)
                    plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_dependence.png')
                    plt.close()
                else:
                    shap.summary_plot(shap_values, X_test, feature_names=X_train.columns, plot_type="bar", show=False)
                    plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_summary.png')
                    plt.close()


                    # SHAP Force Plot for a single instance
                    shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0], feature_names=X_train.columns, matplotlib=True)
                    plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_force.png')
                    plt.close()

                    # SHAP Dependence Plot for the first feature (you can loop over other features)
                    shap.dependence_plot(0, shap_values, X_test, feature_names=X_train.columns, show=False)
                    plt.savefig(f'../plots/{dataset_name}_{model_name}_shap_dependence.png')
                    plt.close()


            except Exception as e:
                print(f"SHAP calculation fialed for {model_name} on {dataset_name}: {e}")

            try:
                i=0
                lime_exp = lime_explainer.explain_instance(X_test.iloc[i].values, model.predict_proba)
                lime_explanations[dataset_name][model_name] = lime_exp

                lime_exp.save_to_file(f'../lime_explanations/{dataset_name}_{model_name}_lime.html')

                # LIME Feature Importance Plot
                lime_exp.as_pyplot_figure()
                plt.savefig(f'../plots/{dataset_name}_{model_name}_lime_feature_importance.png')
                plt.close()

            except Exception as e:
                print(f'LIME explanation failed for {model_name} on {dataset_name} : {e}')

        reports[dataset_name] = dataset_reports
        shap_values_dict[dataset_name] = shap_values_dict

    return reports, shap_values_dict, lime_explanations
