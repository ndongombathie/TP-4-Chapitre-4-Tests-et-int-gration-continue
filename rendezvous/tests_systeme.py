"""
TP4, partie 2 — Test système (chapitre 4).

Un test système exerce l'application ENTIÈRE, de bout en bout, comme le
ferait un utilisateur : formulaire -> soumission -> facture. Contrairement
aux tests unitaires (TP1/TP2) ou aux tests d'intégration vue par vue
(TP3), on ne teste pas ici un composant isolé, mais l'enchaînement complet
à travers plusieurs apps (patients + rendezvous).

TODO (TP4) : écrivez un test qui, dans une seule méthode :
1. crée un patient (Patient.objects.create)
2. affiche le formulaire de prise de rendez-vous (GET /rendezvous/) et
   vérifie que le patient y apparaît
3. soumet une prise de rendez-vous (POST /rendezvous/)
4. consulte la facture du patient (GET /rendezvous/facture/<id>/) et
   vérifie que le total affiché correspond au tarif attendu

Comparez avec solution/rendezvous/tests_systeme.py une fois terminé.
"""
from datetime import date

from django.test import TestCase

from patients.models import Patient
from rendezvous.models import RendezVous


class ParcoursCompletRendezVousTest(TestCase):
    def test_parcours_complet_de_la_prise_de_rendez_vous_a_la_facture(self):
        # 1. Créer un patient
        patient = Patient.objects.create(
            nom="Diallo",
            prenom="Aminata",
            email="aminata@example.com",
            est_vip=False,
        )

        # 2. Afficher le formulaire et vérifier que le patient y apparaît
        response = self.client.get("/rendezvous/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, patient.prenom)
        self.assertContains(response, patient.nom)

        # 3. Soumettre une prise de rendez-vous
        date_rdv = date(2026, 9, 14)  # lundi → pas de majoration weekend
        response = self.client.post(
            "/rendezvous/",
            {
                "patient": patient.pk,
                "type_consultation": "GENERALISTE",
                "date": date_rdv.isoformat(),
                "notes": "Consultation de contrôle",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirection après POST

        self.assertTrue(
            RendezVous.objects.filter(patient=patient).exists(),
            "Le rendez-vous devrait avoir été créé en base",
        )

        # 4. Consulter la facture et vérifier le total
        response = self.client.get(f"/rendezvous/facture/{patient.pk}/")
        self.assertEqual(response.status_code, 200)

        rendez_vous = RendezVous.objects.get(patient=patient)
        self.assertEqual(rendez_vous.prix, 5000)  # tarif généraliste, jour ouvré

        self.assertContains(response, "5000")
        self.assertContains(response, "FCFA")
