class Course:
    def __init__(self, circuit, pilotes):
        self.circuit = circuit
        self.pilotes = pilotes

    def lancer(self):
        print("\n================================")
        print("       DÉPART DE LA COURSE")
        print("================================")

        print(f"Circuit : {self.circuit.nom}")
        print(f"Nombre de tours : {self.circuit.nombre_tours}")

        print("\nParticipants :")

        for i, pilote in enumerate(self.pilotes):
            if i == 1 and len(self.pilotes) == 2:
                print(f"- {pilote.nom} avec {pilote.voiture.marque} (ORDINATEUR)")
            else:
                print(f"- {pilote.nom} avec {pilote.voiture.marque} (JOUEUR {i+1})")

        print("\n🏁 Que la course commence !")