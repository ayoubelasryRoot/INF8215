from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
from math import exp, log

class SoftmaxClassifier(BaseEstimator, ClassifierMixin):  

    def __init__(self, lr = 0.1, alpha = 100, n_epochs = 5, eps = 1.0e-5,threshold = 1.0e-10 , early_stopping = True):
       
        self.lr = lr 
        self.alpha = alpha
        self.n_epochs = n_epochs
        self.eps = eps
        self.threshold = threshold
        self.early_stopping = early_stopping
        


    """
        In:
        X : l'ensemble d'exemple de taille nb_example x nb_features
        y : l'ensemble d'étiquette de taille nb_example x 1

        Principe:
        Initialiser la matrice de poids
        Ajouter une colonne de bias à X
        Pour chaque epoch
            calculer les probabilités
            calculer le log loss
            calculer le gradient
            mettre à jouer les poids
            sauvegarder le loss
            tester pour early stopping

        Out:
        self, in sklearn the fit method returns the object itself
    """

    def get_nb_classes(self, y):
        if y is None:
            return -1
        return len(np.unique(y))


    def fit(self, X, y=None):
        
        prev_loss = np.inf
        self.losses_ = []

        X_bias = np.c_[np.ones(len(X)) , X]  

        self.nb_feature = len(X[0]) + 1
        self.nb_classes = self.get_nb_classes(y)

        # create weigth matrix
        self.theta_ = np.random.rand(self.nb_feature, self.nb_classes)
        one_hot_encoding = self._one_hot(y)

        for epoch in range(self.n_epochs):
            probabilities = self.predict_proba(X, None)      
            prev_loss = self._cost_function(probabilities, one_hot_encoding)   
            self.theta_ = self.theta_ - self.lr*self._get_gradient(X_bias, one_hot_encoding, probabilities)
            
            new_loss = self.score(X, one_hot_encoding)
            if self.early_stopping and abs(prev_loss - new_loss) < self.threshold:
                break

        return self


    def predict_proba(self, X, y=None):
        try:
            getattr(self, "theta_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")
        
        X_bias = np.c_[np.ones(len(X)), X]
        Z = np.dot(X_bias, self.theta_)
        P_matrix = []
        for z in Z:
            P_matrix.append(self._softmax(z))
        return np.array(P_matrix)


    
    def predict(self, X, y=None):
        try:
            getattr(self, "theta_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")
        #X_bias = np.c_[np.ones(len(X)) , X]
        P_matrix = self.predict_proba(X, y)
        return np.argmax(P_matrix, axis=1)

    
    def fit_predict(self, X, y=None):
        self.fit(X, y)
        return self.predict(X,y)
 

    def score(self, X_bias, one_hot_encoding=None):
        #predicted_classes = np.dot(X_bias , self.theta_)
        probabilities = self.predict_proba(X_bias, one_hot_encoding)
        loss = self._cost_function(probabilities, one_hot_encoding)
        return loss
    
    def _cost_function(self, probabilities, one_hot_encoding): 
        m = len(one_hot_encoding)
        cross_sum = 0
        for i in range(m):
            p = np.log(probabilities[i])
            y_i = one_hot_encoding[i]
            cross_sum += np.dot(y_i, p)
        return (-1 / m) * cross_sum
    

    def _one_hot(self, y):
        matrix=np.zeros((len(y), self.nb_classes))
        for i in range(len(y)):
            matrix[i][y[i]] = 1
        return matrix

    
    def _softmax(self, z):
        p = np.zeros(len(z))
        # get exp sum
        sum_softmax = 0
        for value in z:
            sum_softmax += exp(value)
        # proba of zk   
        for k, value in enumerate(z):
            proba_zk = exp(value) / sum_softmax
            if proba_zk == 0:
                proba_zk = self.eps
            if proba_zk >= 1:
                proba_zk = 1 - self.eps
            p[k] = proba_zk
        return p


    def _get_gradient(self,X_bias, one_hot_encoding, probabilities):
        m = len(X_bias)
        return (1/m) * np.dot(np.transpose(X_bias), (probabilities - one_hot_encoding))
    