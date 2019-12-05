import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from SoftmaxClassifier import SoftmaxClassifier
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# load dataset
data,target =load_iris().data,load_iris().target

# split data in train/test sets
X_train, X_test, y_train, y_test = train_test_split( data, target, test_size=0.33, random_state=42)

# standardize columns using normal distribution
# fit on X_train and not on X_test to avoid Data Leakage
s = StandardScaler()
X_train = s.fit_transform(X_train)
X_test = s.transform(X_test)

cl = SoftmaxClassifier()

# train on X_train and not on X_test to avoid overfitting
train_p = cl.fit_predict(X_train,y_train)
test_p = cl.predict(X_test)

print(test_p)



PATH = "C:/Users/USER/Desktop/INF8215/INF8215/tp3/" # changer le path avec votre path
X_train = pd.read_csv(PATH + "adult.csv", encoding="utf-8-sig")
X_test = pd.read_csv(PATH + "adult.csv")

y_train = X_train['income']

from sklearn.base import BaseEstimator, TransformerMixin
## Wrapper pour vous aider pour les pipelines
class TransformationWrapper(BaseEstimator,TransformerMixin):
    
    def __init__(self,fitation= None, transformation = None): 
        
        self.transformation = transformation
        self.fitation = fitation
        
    
        
    def fit(self, X, y=None):
        X = pd.DataFrame(X)
        self.data_ = None
        self.column_name_ = X.columns[0]
        if self.fitation == None:
            return self
        
        self.data_ = [self.fitation(X[self.column_name_])]
        return self  
    
    def transform(self, X, y=None): 
        X = pd.DataFrame(X)
        
        if self.data_ != None:
            return pd.DataFrame(X.apply(
                lambda row: pd.Series( self.transformation(row[self.column_name_], self.data_)),
                axis = 1
            ))
        else:
            return pd.DataFrame(X.apply(
                lambda row: pd.Series( self.transformation(row[self.column_name_])),
                axis = 1
            ))
        
        
from sklearn.preprocessing import LabelEncoder
class LabelEncoderP(LabelEncoder):
    def fit(self, X, y=None):
        super(LabelEncoderP, self).fit(X)
    def transform(self, X, y=None):
        return pd.DataFrame(super(LabelEncoderP, self).transform(X))
    def fit_transform(self, X, y=None):
        return super(LabelEncoderP, self).fit(X).transform(X)

        # Implémenter ici les différentes transformations customs ici pour que cela soit plus claires (Si vous en avez)

def country_data_transformation(country):
    if country == 'United-states':
        return country
    else: return 'Other'


from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

pipeline_country = Pipeline([
    ("fill", SimpleImputer(strategy = 'constant', fill_value = "United-States")),
    ('country', TransformationWrapper(transformation = country_data_transformation)),
    ("encode",LabelEncoderP()),
])

pipeline_final_weight = Pipeline([
    ("fillna", SimpleImputer(strategy = 'mean') ),
    ("scaler",StandardScaler())
])

pipeline_capital_gain = Pipeline([
    ("fillna", SimpleImputer(strategy = 'mean') ),
    ("scaler",StandardScaler())
])


pipeline_capital_loss = Pipeline([
    ("fillna", SimpleImputer(strategy = 'mean') ),
    ("scaler",StandardScaler())
])

pipeline_hours_per_week = Pipeline([
    ("fillna", SimpleImputer(strategy = 'mean') ),
    ("scaler",StandardScaler())
])

pipeline_age = Pipeline([
    ("fillna", SimpleImputer(strategy = 'mean') ),
    ("scaler",StandardScaler())
])

pipeline_education = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'Bachelors')),
    ("encode",OneHotEncoder(categories = 'auto', sparse = False))
])

pipeline_sex = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'Male')),
    ("encode",LabelEncoderP())
])

pipeline_race = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'White')),
    ("encode",OneHotEncoder(categories = 'auto', sparse = False))
])


pipeline_marital_status = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'Never-Married')),
    ("encode",OneHotEncoder(categories = 'auto', sparse = False))
])


pipeline_workclass = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'Private')),
    ("encode",OneHotEncoder(categories = 'auto', sparse = False))
])

pipeline_occupation = Pipeline([
    ("fillna", SimpleImputer(strategy = 'constant', fill_value = 'Prof-specialty')),
    ("encode",OneHotEncoder(categories = 'auto', sparse = False))
])


full_pipeline = ColumnTransformer([
         ("native.country", pipeline_country, ["native.country"]),
         ("fnlwgt", pipeline_final_weight, ["fnlwgt"]),
         ("capital.gain", pipeline_capital_gain, ["capital.gain"]),
         ("capital.loss", pipeline_capital_loss, ["capital.loss"]),
         ("hours.per.week", pipeline_hours_per_week, ["hours.per.week"]),
         ("age", pipeline_age, ["age"]),
         ("education", pipeline_education, ["education"]),
         ("sex", pipeline_sex, ["sex"]),
         ("race", pipeline_race, ["race"]),
         ("occupation", pipeline_occupation, ["occupation"]),
         ("marital.status", pipeline_marital_status, ["marital.status"]),
         ("workclass", pipeline_workclass, ["workclass"]),
    ])

column_names = ['Native Country', 'Final Weight', 'Capital Gain', 'Capital Loss' , 'Hours Per Week', 'Age', 'Education_1', 
                'Education_2', 'Education_3', 'Education_4', 'Education_5', 'Education_6', 'Education_7', 'Education_8', 
                'Education_9', 'Education_10', 'Education_11', 'Education_12', 'Education_13', 'Education_14', 'Education_15', 
                'Education_16', 'Sex', 'Race_1', 'Race_2', 'Race_3', 'Race_4', 'Race_5', 'Occupation_1', 'Occupation_2', 'Occupation_3',
                'Occupation_4', 'Occupation_5', 'Occupation_6', 'Occupation_7', 'Occupation_8', 'Occupation_9', 'Occupation_10', 'Occupation_11',
                'Occupation_12', 'Occupation_13', 'Occupation_14', 'Occupation_15', 'Marital_status_1','Marital_status_2','Marital_status_3',
               'Marital_status_4','Marital_status_5','Marital_status_6','Marital_status_7', 'Workclass_1', 'Workclass_2', 'Workclass_3',
               'Workclass_4', 'Workclass_5', 'Workclass_6', 'Workclass_7', 'Workclass_8', 'Workclass_9'] # TODO ajouter les noms des colonnes selon le nouvel ordre du pipeline
X_train_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_train), columns=column_names)
X_test_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_test), columns=column_names)

X_train_preprocess.head()

target_label = LabelEncoder()
y_train_label = target_label.fit_transform(y_train)
print(target_label.classes_)



from sklearn.model_selection import cross_validate
def compare(models,X_train,y_train,nb_runs,scoring):
    scores = []
    for model in models:
        cv_scores = cross_validate(model, X_train, y_train, scoring=scoring, cv = nb_runs)
        print("HEYOO")
        for key in cv_scores:
            mean = np.mean(cv_scores[key])
            standardDeviation = np.std(cv_scores[key])
            cv_scores[key] = { 'mean' : mean, 'standardDeviation' : standardDeviation}
        scores.append(cv_scores)
        
    return scores


from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

nb_run = 3

models = [
    #DecisionTreeClassifier(),
    #LogisticRegression(),
    SoftmaxClassifier() # le modele que vous avez implémenté plus haut
]

scoring = ['neg_log_loss', 'precision_macro','recall_macro','f1_macro']

compare(models,X_train_preprocess.to_numpy(),y_train_label,nb_run, scoring)





