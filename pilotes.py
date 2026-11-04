
class Pilote:
    def __init__(self, nom, niveau):
        self.nom = nom
        self.niveau = niveau
        self.voiture = None

    def choisir_voiture(self, voiture):
        self.voiture = voiture

pilote_1 = Pilote("Charles Leclerc", 9)
pilote_2=Pilote("Lewis Hamilton",10)
pilote_3=Pilote("George Russell",16)
pilote_4=Pilote("Kimi Antonelli",39)
pilote_5=Pilote("Lando Norris",30)
pilote_6=Pilote("Oscar Piastri",19)
pilote_7=Pilote("Max Verstappen",30)
pilote_8=Pilote("Isack Hadjar",25)

PILOTES = {
    "Ferrari":[pilote_1,pilote_2],
    "Mercedes":[pilote_3,pilote_4],
    "McLaren":[pilote_5,pilote_6],
    "Red Bull":[pilote_7,pilote_8]
}
