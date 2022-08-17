import math as m
import random as rd
# import mysql.connector
# from geopy.geocoders import Nominatim # importing geopy library

infinite = 99999

class Vehicule:
    Masters = []
    Vehicules = []
    k = 12
    rang =11
    w1 ,w2 ,w3 , w4 = 0.25 , 0.25,0.25,0.25
    def __init__(self ):
        self.nom = "Ferrari"
        self.vit = rd.randint(50 ,110)
        self.Svi = self.vit
        self.X , self.Y = rd.sample(range(1, 100), 2)
        self.state = "ND"
        self.numbLien = 0
        self.k_voisin = []
        self.ijma3a = []
        self.weight=infinite
        self.M = infinite
        Vehicule.Vehicules.append(self)
        self.cluster = []
        self.mymaster = self



    def receive(self):
        pass
    def send(self):
        pass

    def Get_speed(Sv):
        pass  # bel GPS ne5thouha mais allahou a3lam kifeh

    def Get_position(self):
        # # from geopy.geocoders import Nominatim # importing geopy library
        #
        # # calling the Nominatim tool
        # loc = Nominatim(user_agent="GetLoc")
        #
        # # entering the location name
        # getLoc = loc.geocode("Gosainganj Lucknow")
        #
        # # printing address
        # print(getLoc.address)
        #
        # # printing latitude and longitude
        # print("Latitude = ", getLoc.latitude, "\n")
        # print("Longitude = ", getLoc.longitude)
        pass

    def distance( self  , v2 ):
        # distance euclidienne
        return m.sqrt((self.X - v2.X) ** 2 + (self.Y - v2.Y) ** 2)

    def K_voisin (self ) :
        ind = [Vehicule.Vehicules.index(v) for v in Vehicule.Vehicules if (self.distance(v) < Vehicule.k) and v != self]
        k_voisin = [Vehicule.Vehicules[i] for i in ind]
        return k_voisin
    def Ijma3a(self):
        ind = [self.k_voisin.index(v) for v in self.k_voisin if (self.distance(v) < Vehicule.rang) and (v.state =="ND") and v != self]
        ijma3a = [self.k_voisin[i] for i in ind]
        return ijma3a
    #TODO: cluster array kan fama mochkol
    def passerelle(self):
        ind = [self.ijma3a.index(v) for v in self.ijma3a if ( Vehicule.rang-3 < self.distance(v) < Vehicule.rang)]
        return [self.ijma3a[i] for i in ind]

    def Density_value(self):
        if (len(self.ijma3a) > 0):
            return len(self.ijma3a) / len(self.k_voisin)
        else : return 1
        # e: lien entre deux nœuds a et b à l'instant t
        # E: ensemble des liens entre nœuds
        # C(𝒗𝒊): rensemble des k-voisins du nœud 𝑣𝑖
        # 𝑑𝑣𝑖: degré du nœud 𝑣𝑖 (le nombre de nœuds dans son k-voisinage)
        # D_Vi=|e=(a,b)in E, a in{V, C(vi)} b in C(vi)|/dvi
        # nombre de liens / voisins
        # dvi = self.nb_neighborhood()
        # # nombre de liens du cluster
        # e = 0
        # visited_nodes = {vi}
        # for v in vi.neighborhood:
        #     for v_ in v.neighborhood:
        #         e += (v_ not in visited_nodes)
        #
        #     visited_node.add(v)
        #
        # # calcul metrique de densite
        # return e / dvi + 1

    def Position_value(self):
        # ************(X_i^max,Y_i^max): position du nœud qui a la plus grande distance à la position moyenne des voisins du nœud vi
        # (𝑥𝑗, 𝑦𝑗): coordonnée de position de tout voisin vj du nœud vi
        # (𝑥i, 𝑦i) la coordonnée de position du nœud vi
        # X_i^u = "Somme de j=1 à N" X_j / N
        # Y_i^u = "Somme de j=1 à N" Y_j / N
        # P_vi = math.sqrt((X_i-X_i^u)**2+(Y_i-Y_i^u)**2)/math.sqrt((X_i^max-X_i^u)**2+(Y_i^max-Y_i^u)**2)  ********
        # calcul position moyenne
        n, x, y = len(self.k_voisin), 0, 0
        for v in self.k_voisin:
            x += v.X
            y += v.Y
        x_mean, y_mean = x / n, y / n

        # calcul distance de noeud la plus eloignee de la position moyenne
        x_max  = max  ([ v.X for v in self.k_voisin ]  )
        y_max  = max  ([ v.Y for v in self.k_voisin ]  )
        # calcul metrique de position
        if (x_max != x_mean and y_max != y_mean ) :
            return m.sqrt((self.X - x_mean )**2 + ((self.Y - y_mean )**2 )) / m.sqrt((x_max - x_mean )**2 + ((y_max - y_mean )**2 ))
        return 0
    def Mobility_value(self):
        Svi_list= [v.Svi for v in self.k_voisin]
        Svi_list.append(self.Svi)
        if (len(self.k_voisin) != 0) :
            uvi  = sum (Svi_list) / len(self.k_voisin)
        else : uvi=0
        return abs ( (self.Svi - uvi) / max ( Svi_list) - uvi)

    def Delay_value(self):
        PL = 80
        B = 160
        TD = PL / B
        nb_packet = rd.randint(0, 7)
        Qd = ((nb_packet - 1) * PL) / (2 *B)
        return TD + Qd

    def Weight_value_W(self):
        return self.w1*(1/self.Density_value()) + self.w2*self.M + self.w3 * self.Position_value() + self.w4 * self.Delay_value()

    def bonjour(self):
        self.k_voisin= self.K_voisin()
        self.ijma3a = self.Ijma3a()




    def algo1(self ):
        self.bonjour()
        self.M = self.Mobility_value()
        if (len(self.k_voisin) > 0) :
            self.weight  =self.Weight_value_W()

    def msg_elect(self):
        for v in self.ijma3a:
            if (v.state == "ND"):
                v.state = "CM"
                print((v.X , v.Y) , "changed to CM")
                v.mymaster=self
                self.cluster.append(v)

    def algo2(self):
        for v in self.k_voisin  :
            if (v.state != "ND"  and self.weight > v.weight):
                return 0
        self.msg_elect()
        self.state = "CH"
        Vehicule.Masters.append(self)

    def alg3 (self):
        if (self.state == 'CM'):
            for v in Vehicule.Masters :
                if ((self.distance(v) < self.rang) and (v.weight < self.mymaster.weight)):
                    if (self.weight >= v.weight):
                        self.mymaster.cluster.remove(self)
                        self.mymaster=v
                        self.mymaster.cluster.append(self)
                    else:
                        self.algo2()
        elif (self.state == 'ND'):
            if (len(self.k_voisin) > 0):
                self.algo2()




    def algo4 (self):
        for ch in Vehicule.Masters :
            marge = ch.passerelle()
            P_min = marge[0]
            for p in marge[1 :] :
                if (p.M < P_min.M):
                    P_min = p
            p.state = "Gate"

vehicules = [Vehicule() for i in range (200)]
