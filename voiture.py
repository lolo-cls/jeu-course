class Voiture:
    def __init__(self, marque, vitesse_max, acceleration):
        self.marque = marque
        self.vitesse_max = vitesse_max
        self.acceleration = acceleration
        self.vitesse = 0

    def accelerer(self):
        self.vitesse += self.acceleration
        if self.vitesse > self.vitesse_max:
            self.vitesse = self.vitesse_max

   def freiner(self, freinage=10):
    self.vitesse -= freinage
    if self.vitesse < 0:
        self.vitesse = 0 

pilote_1 = Voiture("Ferrari",320,25)
pilote_2 = Voiture("Mercedes",300,30)
pilote_3=Voiture("Mclaren",200,40)
pilote_4=Voiture("Redbull",140,28)
