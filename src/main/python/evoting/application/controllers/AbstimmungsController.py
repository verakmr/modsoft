from src.main.python.evoting.domain.entities.Abstimmung import Abstimmung
from src.main.python.evoting.application.dekoratoren.dekoratoren import log_method_call, handle_exceptions
from src.main.python.evoting.infrastructure.services.AbstimmungsService import AbstimmungService
from src.main.python.evoting.infrastructure.repositories.AbstimmungRepository import AbstimmungRepository
from src.main.python.evoting.infrastructure.services.UserService import BuergerService

class AbstimmungController:
    """
    Schnittstelle für Abstimmungsoperationen, z. B. für Webanwendungen oder APIs.
    Delegiert die Geschäftslogik an den Service und formatiert die Ergebnisse.
    """

    @log_method_call
    @handle_exceptions
    def __init__(self):
        self.service = AbstimmungService(AbstimmungRepository())
        self.buerger_service = BuergerService()

    @log_method_call
    @handle_exceptions
    def erstelle_abstimmung(self, abstimmung_data):
        """
        Erstellt eine neue Abstimmung.
        :param abstimmung_data: Ein Dictionary mit Abstimmungsdetails.
        :return: Ein Erfolgs- oder Fehlermeldungs-Dictionary.
        """
        try:
            abstimmung = Abstimmung(
                abstimmungid=abstimmung_data["abstimmungid"],
                titel=abstimmung_data["titel"],
                beschreibung=abstimmung_data["beschreibung"],
                frist=abstimmung_data["frist"],
                altersgrenze=abstimmung_data["altersgrenze"],
                status=abstimmung_data["status"]
            )
            self.service.erstelle_abstimmung(abstimmung)
            return {"message": "Abstimmung erfolgreich erstellt!", "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    @log_method_call
    @handle_exceptions
    def finde_abstimmung(self, abstimmungid):
        """
        Sucht eine Abstimmung basierend auf der Abstimmungs-ID.
        :param abstimmungid: Die ID der Abstimmung.
        :return: Ein Dictionary mit Abstimmungsdetails oder einer Fehlermeldung.
        """
        try:
            abstimmung = self.service.finde_abstimmung(abstimmungid)
            return {
                "abstimmungid": abstimmung.abstimmungid,
                "titel": abstimmung.titel,
                "beschreibung": abstimmung.beschreibung,
                "frist": abstimmung.frist.strftime("%Y-%m-%d"),
                "altersgrenze": abstimmung.altersgrenze,
                "status": abstimmung.status,
            }
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    @log_method_call
    @handle_exceptions
    def aktualisiere_abstimmung(self, abstimmungid, updates):
        """
        Aktualisiert eine Abstimmung.
        :param abstimmungid: Die ID der Abstimmung, die aktualisiert werden soll.
        :param updates: Ein Dictionary mit den zu aktualisierenden Feldern.
        :return: Ein Erfolgs- oder Fehlermeldungs-Dictionary.
        """
        try:
            self.service.aktualisiere_abstimmung(abstimmungid, **updates)
            return {"message": f"Abstimmung mit ID {abstimmungid} erfolgreich aktualisiert!", "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    @log_method_call
    @handle_exceptions
    def entferne_abstimmung(self, abstimmungid):
        """
        Entfernt eine Abstimmung basierend auf der Abstimmungs-ID.
        :param abstimmungid: Die ID der zu entfernenden Abstimmung.
        :return: Ein Erfolgs- oder Fehlermeldungs-Dictionary.
        """
        try:
            self.service.entferne_abstimmung(abstimmungid)
            return {"message": f"Abstimmung mit ID {abstimmungid} erfolgreich entfernt!", "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    @log_method_call
    @handle_exceptions
    def finde_abstimmungen_fuer_buerger(self, email, passwort):
        """
        Gibt eine Liste von Abstimmungen zurück, die für einen bestimmten Bürger zugänglich sind,
        basierend auf der Altersgrenze.
        :param email: Die E-Mail des Bürgers
        :param passwort: Das Passwort des Bürgers
        :return: Eine Liste von Abstimmungen, die der Bürger sehen kann.
        """
        try:
            buerger = self.buerger_service.finde_buerger(email, passwort)
            alter = buerger.alter  # Angenommen, du hast eine 'alter'-Eigenschaft in der 'Buerger' Klasse
            abstimmungen = self.service.finde_alle_abstimmungen()

            # Filtere die Abstimmungen basierend auf der Altersgrenze
            filter_abstimmungen = [
                abstimmung for abstimmung in abstimmungen if abstimmung.altersgrenze <= alter
            ]

            return [
                {
                    "abstimmungid": abstimmung.abstimmungid,
                    "titel": abstimmung.titel,
                    "beschreibung": abstimmung.beschreibung,
                    "frist": abstimmung.frist.strftime("%Y-%m-%d"),
                    "altersgrenze": abstimmung.altersgrenze,
                    "status": abstimmung.status,
                }
                for abstimmung in filter_abstimmungen
            ]

        except Exception as e:
            return {"error": str(e)}

    @log_method_call
    @handle_exceptions
    def abstimmen(self, abstimmungid, buergerid):
        """
        Ermöglicht einem Bürger, an einer Abstimmung teilzunehmen.
        :param abstimmungid: Die ID der Abstimmung.
        :param buergerid: Die ID des Bürgers.
        """
        try:
            abstimmung = self.service.finde_abstimmung(abstimmungid)
            if abstimmung.status != "aktiv":
                raise ValueError("Die Abstimmung ist nicht mehr aktiv.")
            self.service.abstimmen(abstimmungid, buergerid)
            return {"message": "Erfolgreich abgestimmt!", "status": "success"}
        except Exception as e:
            self.logger.error(f"Fehler beim Abstimmen: {e}")
            return {"error": str(e), "status": "failure"}