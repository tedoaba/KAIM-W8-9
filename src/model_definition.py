from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

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

    for dataset_name, (X_train, y_train, X_test, y_test) in datasets.items():
        dataset_reports = []
        for model_name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            dataset_reports.append((model_name, model, report))
        reports[dataset_name] = dataset_reports

    return reports
