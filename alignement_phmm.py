# -*-coding:utf-8-*-


import enum
import numpy as np
import numpy.random as nr
from utils import *

# alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# atomes des mots


class MatriceEmissionCouple:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.n = len(alphabet)
        self.mat = np.zeros((self.n, self.n))

    def get_emission_matrix(self):
        return self.mat

    def set_emission_matrix(self, mat):
        self.mat = mat

    def __getitem__(self, item):
        return self.mat

    def __len__(self):
        return self.n

class MatriceEmissionSimple:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.n = len(alphabet)
        self.mat = np.zeros((self.n,))

    def get_emission_matrix(self):
        return self.mat

    def set_emission_matrix(self, mat):
        self.mat = mat

    def __getitem__(self, item):
        return self.mat

    def __len__(self):
        return self.n


class MatriceTransition:
    def __init__(self, epsilon, delta, tau_m, tau_is, _lambda):
        self.epsilon = epsilon
        self.delta = delta
        self.tau_m = tau_m
        self.tau_is = tau_is
        self._lambda = _lambda
        self.freq_transitions = np.zeros((3, 3))
        # def add_transition(self, l, m):

    def get_values(self):
        return self.epsilon, self.delta, self.tau_m, self.tau_is, self._lambda

    def update_epsilon(self):
        nume = self.freq_transitions[Etats.INSERTION, Etats.INSERTION] + self.freq_transitions[Etats.SUPPRESSION, Etats.SUPPRESSION]
        denomi = np.sum(self.freq_transitions[Etats.INSERTION, :]) + np.sum(self.freq_transitions[Etats.SUPPRESSION, :])
        self.epsilon = nume / denomi

    def update_delta(self):
        nume = self.freq_transitions[Etats.CORRESPONDANCE, Etats.INSERTION] + self.freq_transitions[Etats.CORRESPONDANCE, Etats.SUPPRESSION]
        denomi = np.sum(self.freq_transitions[Etats.CORRESPONDANCE, :])
        self.delta = nume /denomi

    def update_tau_m(self, n_m_fin):
        nume = n_m_fin
        denomi = n_m_fin + np.sum(self.freq_transitions[Etats.CORRESPONDANCE, :])
        self.tau_m = nume / denomi

    def update_tau_is(self, n_is_fin):
        nume = n_is_fin
        denomi = n_is_fin + np.sum(self.freq_transitions[Etats.INSERTION, :]) + np.sum(self.freq_transitions[Etats.SUPPRESSION, :])
        self.tau_is = nume / denomi

    def update_lambda(self):
        nume = self.freq_transitions[Etats.E_INSER, Etats.SUPPRESSION] + self.freq_transitions[Etats.SUPPRESSION, Etats.INSERTION]
        denomi = np.sum(self.freq_transitions[Etats.INSERTION, :]) + np.sum(self.freq_transitions[Etats.SUPPRESSION, :])
        self._lambda = nume / denomi

    def get_transition_matrix(self):
        return np.array([[1-2*self.delta, self.delta, self.delta],
                         [1-self.epsilon-self._lambda, self.epsilon, self._lambda],
                         [1-self._lambda-self.epsilon, self._lambda, self.epsilon]])

    def get_final_transition(self):
        return np.array([self.tau_m, self.tau_is, self.tau_is])

    def update_params(self, n_m_fin, n_is_fin):
        self.update_epsilon()
        self.update_delta()
        self.update_tau_m(n_m_fin)
        self.update_tau_is(n_is_fin)
        self.update_lambda()


class ParametresPHMM:
    def __init__(self, epsilon, delta, tau_m, tau_is, _lambda, pseudo_compte):
        self.mat_trans = MatriceTransition(epsilon, delta, tau_m, tau_is, _lambda)
        self.mat_emi_m = MatriceEmissionCouple(alphabet)
        self.mat_emi_is = MatriceEmissionSimple(alphabet)
        self.pseudo_compte = pseudo_compte

    # def compute_freq_emissions(self, l_couples_alignes):
    #     for phi, chi in l_couples:


    # def get_emission_matrix(self, i_phi, j_khi):
    #     """
    #     p(\khi_i, \psi_j)
    #     :return:
    #     """
    #     nume = self.freq_emission_couple[i_phi, j_khi] + self.pseudo_compte
    #     denomi = np.sum(np.sum(self.freq_emission)) + self.pseudo_compte
    #     return nume / denomi
    #
    # def get_emission_vector(self, carac):
    #     """
    #     p(\khi_i)
    #     :return:
    #     """
    #     nume = self.freq_emission[carac] + self.pseudo_compte
    #     denomi = np.sum(self.freq_emission) + self.pseudo_compte
    #     return nume / denomi

    def update_params(self, n_m_fin, n_is_fin):
        epsilon, delta, tau_m, tau_is, _lambda = self.mat_trans.get_values()
        self.mat_trans.update_params(n_m_fin, n_is_fin)
        diff = abs(epsilon- self.mat_trans.epsilon) + abs(delta - self.mat_trans.delta) + abs(tau_m - self.mat_trans.tau_m) +\
               abs(tau_is - self.mat_trans.tau_is) + abs(_lambda - self.mat_trans._lambda)
        return diff


def compute_forward(phi, khi, mat_tra, mat_emi_m, mat_emi_is, trans_fin):
    alpha = np.zeros((phi.size+1, khi.size+1, mat_tra.shape[0]))
    alpha[0, 0, 0] = 1
    for i in range(phi.size):
        for j in range(khi.size):
            if i == 0 and j == 0:
                continue
            if i == 0:
                alpha[i, j, 0] = 0
                alpha[i, j, 1] = 0
                alpha[i, j, 2] = mat_emi_is[alphabet.index(khi[j])] * \
                                 np.sum(mat_tra[2, :] * alpha[i, j-1, :])
            if j == 0:
                alpha[i, j, 0] = 0
                alpha[i, j, 1] = mat_emi_is[alphabet.index(khi[j])] * \
                                 np.sum(mat_tra[2, :] * alpha[i-1, j, :])
                alpha[i, j, 2] = 0

            else:
                alpha[i, j, 0] = mat_emi_m[alphabet.index(phi[i]), alphabet.index(khi[j])] * \
                                 np.sum(mat_tra[0, :] * alpha[i-1, j-1, :])

                alpha[i, j, 1] = mat_emi_is[alphabet.index(phi[i])] * \
                                 np.sum(mat_tra[1, :] * alpha[i-1, j, :])
                alpha[i, j, 2] = mat_emi_is[alphabet.index(khi[j])] * \
                                 np.sum(mat_tra[2, :] * alpha[i, j-1, :])
                alpha[i, j, :] /= np.sum(alpha[i, j, :])
    alpha_fin = np.sum(trans_fin * alpha[phi.size, khi.size, :])
    return alpha, alpha_fin


def compute_backward(phi, khi, mat_tra, mat_emi_m, mat_emi_is, trans_fin):
    beta = np.zeros((phi.size+1, khi.size+1, mat_tra.shape[0]))
    beta[phi.size, khi.size, :] = trans_fin
    for i in range(phi.size, -1, -1):
        for j in range(khi.size, -1, -1):
            for k in Etats:
                print(mat_emi_m.shape)
                print(mat_emi_is.shape)
                print(mat_emi_m)
                emi = np.array([mat_emi_m[alphabet.index(phi[i+1]), alphabet.index(khi[j+1])],
                                                 mat_emi_is[alphabet.index(phi[i+1])], mat_emi_is[alphabet.index(khi[j+1])]])
                beta_transition = np.array([beta[i+1, j+1, 0], beta[i+1, j, 1], beta[i, j+1, 2]])
                beta[i, j, k] = np.sum((emi * mat_tra[k, :]) * beta_transition)
    return beta


def viterbi(phi, khi, param:ParametresPHMM):
    n = len(phi)
    m = len(khi)

    correspondances = np.zeros((n+1, m+1))
    chemin_correspondance = np.zeros((n+1, m+1))
    insertions = np.zeros((n+1, m+1))
    chemin_insertion = np.zeros((n+1, m+1))
    suppressions  = np.zeros((n+1, m+1))
    chemin_suppression  = np.zeros((n+1, m+1))

    correspondances[0, 0] = 1
    insertions[:, 0] = 0
    insertions[0, :] = 0
    suppressions[:, 0] = 0
    suppressions[0, :] = 0
    chemin_optimal = []

    for i in range(1, n+1):
        for j in range(1, m+1):
            correspondances[i, j] = param.mat_emi_m.mat[alphabet.index(phi[i]), alphabet.index(khi[j])]*np.max([(1-2*param.mat_trans.delta- param.mat_trans.tau_m)* correspondances[i-1, j-1],
                                                                        (1-param.mat_trans.epsilon-param.mat_trans.tau_is - param.mat_trans._lambda) * insertions[i-1, j-1],
                                                                         (1-param.mat_trans.epsilon-param.mat_trans.tau_is - param.mat_trans._lambda) * suppressions[i-1, j-1]])
            chemin_correspondance[i, j] = np.argmax([(1-2*param.mat_trans.delta- param.mat_trans.tau_m)* correspondances[i-1, j-1],
                                                                        (1-param.mat_trans.epsilon-param.mat_trans.tau_is - param.mat_trans._lambda) * insertions[i-1, j-1],
                                                                         (1-param.mat_trans.epsilon-param.mat_trans.tau_is - param.mat_trans._lambda) * suppressions[i-1, j-1]])

            insertions[i, j] = param.mat_emi_is[alphabet.index(khi[j])]*np.max([param.mat_trans.delta* correspondances[i-1, j],
                                                                        param.mat_trans.epsilon * insertions[i-1, j]])
            chemin_insertion[i, j] = np.argmax([param.mat_trans.delta* correspondances[i-1, j], param.mat_trans.epsilon * insertions[i-1, j]])
            suppressions[i, j] = param.mat_emi_is[alphabet.index(khi[j])] * np.max([param.mat_trans.delta* correspondances[i, j-1],
                                                                        param.mat_trans.epsilon * suppressions[i, j-1]])
            chemin_suppression[i, j] = np.argmax([param.mat_trans.delta* correspondances[i, j-1], param.mat_trans.epsilon * suppressions[i, j-1]])

            if i == n and j == m:
                fin = np.max([param.mat_trans.tau_m * correspondances[n, m], param.mat_trans.tau_is*insertions[n, m], param.mat_trans.tau_is*suppressions[n, m]])
                etat_fin = np.argmax([param.mat_trans.tau_m * correspondances[n, m], param.mat_trans.tau_is*insertions[n, m], param.mat_trans.tau_is*suppressions[n, m]])

    i = n
    j = m
    etat = etats[etat_fin[0]]
    chemin_optimal.append(etat)
    while i > 0 and j > 0:
        if etat == "M":
            i -= 1
            j -= 1
            etat = etats[chemin_correspondance[i, j][0]]
        elif etat == "I":
            i -= 1
            etat = etats[chemin_insertion[i, j][0]]
        elif etat == "S":
            j -= 1
            etat = etats[chemin_suppression[i, j][0]]
        chemin_optimal.append(etat)

    return chemin_optimal


def em_phmm_alphabeta(l_paires):
    precision = 0.02
    diff = 0.3

    # Initialisation
    pseudo_compte = 0.0001
    param = ParametresPHMM(nr.random(), nr.random(), nr.random(), nr.random(), nr.random(), pseudo_compte)

    while diff > precision:
        ksis = []
        gammas = []
        for h in range(len(l_paires)):
            phi, khi = l_paires[h]
            alpha, alpha_fin = compute_forward(phi, khi, param.mat_trans.get_transition_matrix(), param.mat_emi_m.mat,
                                    param.mat_emi_is.mat, param.mat_trans.get_final_transition())
            beta = compute_backward(phi, khi, param.mat_trans.get_transition_matrix(), param.mat_emi_m.mat,
                                    param.mat_emi_is.mat , param.mat_trans.get_final_transition())

            transi = param.mat_trans.get_transition_matrix()

            ksis.append(np.zeros((len(phi), len(khi), 3, 3)))
            gammas.append(np.zeros((len(phi), len(khi), 3)))

            for i in range(len(phi)):
                for j in range(len(khi)):
                    for l in Etats:
                        # calcul de probabilités de transition
                        ksis[h][i, j, l, Etats.CORRESPONDANCE] = alpha[i, j, l] * transi[l, Etats.CORRESPONDANCE] * param.mat_emi_m[phi[i], khi[j]] * beta[i, j, Etats.INSERTION]
                        ksis[h][i, j, l, Etats.INSERTION] = alpha[i, j, l] * transi[l, Etats.INSERTION] * param.mat_emi_is[phi[i]] * beta[i, j, Etats.INSERTION]
                        ksis[h][i, j, l, Etats.SUPPRESSION] = alpha[i, j, l] * transi[l, Etats.SUPPRESSION] * param.mat_emi_is[khi[i]] * beta[i, j, Etats.SUPPRESSION]
                        ksis[h][i, j, l, :] /= alpha_fin  # normalisation
                        gammas[h][i, j, l] = alpha[i, j, l]*beta[i, j, l]
                        # probabilité  d'un état sachant les deux séquences
                    gammas[h][i, j, :] /= np.sum(alpha[i, j, :]*beta[i, j, :])  # normalisation

        # M

        # estimation de la matrice de transition
        a = np.zeros((3, 3))
        for l in Etats:
            for m in Etats:
                a[l, m] = np.sum([np.sum(np.sum(ksis[h][:, :, l, m])) for h in range(len(l_paires))])
            a[l, :] /= np.sum(a[l, :])
        # instancier a dans param de manière correcte !
        # il faut convertir la matrice de transition en paramètres de cette matrice


        # émission dans le cas d'un alignement
        pi_m = np.zeros((len(alphabet), len(alphabet)))
        pi_is = np.zeros((2, len(alphabet)))
        for carac_1 in range(len(alphabet)):
            for carac_2 in range(len(alphabet)):
                for h in range(len(l_paires)):
                    phi, khi = l_paires[h]
                    for i in range(len(phi)):
                        for j in range(len(khi)):
                            pi_m[carac_1, carac_2] = gammas[h][i, j, l] * delta(phi[i] == alphabet[carac_1]) * delta(khi[j] == alphabet[carac_2])

        # émission dans le cas d'une insertion et  d'une suppression
        for carac in range(len(alphabet)):
            for h in range(len(l_paires)):
                phi, khi = l_paires[h]
                for i in range(len(phi)):
                    pi_is[Etats.INSERTION, carac] = np.sum(gammas[h][i, :, l]) * delta(phi[i] == alphabet[carac])
                for j in range(len(khi)):
                    pi_is[Etats.SUPPRESSION, carac] = np.sum(gammas[h][:, j, l]) * delta(khi[j] == alphabet[carac])

        param.mat_emi_m.set_emission_matrix(pi_m)
        param.mat_emi_m.set_emission_matrix(pi_is)
        # diff = param.update_params(n_m_fin, n_is_fin)

    return param


if __name__ == "__main__":
    # l_paires = []
    # param, freq_emissions = em_phmm(l_paires)
    # mot1 = ""
    # mot2 = ""
    # meilleur_alignement = viterbi(mot1, mot2, param, freq_emissions)
    # print(mot1)
    # print(mot2)
    # print(meilleur_alignement)

    test_liste_vers_paries()