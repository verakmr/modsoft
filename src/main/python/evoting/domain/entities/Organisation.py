class Organisation:
    def __init__(self, citizens_id, name, email, password, authentifizierungsstatus, stimmberechtigung):
        self.citizens_id = citizens_id
        self.name = name
        self.email = email
        self.password = password
        self.authentifizierungsstatus = authentifizierungsstatus
        self.stimmberechtigung = stimmberechtigung