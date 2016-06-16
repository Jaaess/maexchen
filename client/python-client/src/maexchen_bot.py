import signal
import sys
import socket

from udp_kommunikator import UDP_Kommunikator


class Maexchen_Bot:
    def __init__(self, server_ip="127.0.0.1", server_port=9000):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.kommunikator = UDP_Kommunikator(server_ip=server_ip, server_port=server_port)

    def warte_auf_nachricht(self):
        try:
            (nachricht, parameter) = self.kommunikator.warte_auf_nachricht()
            print("Nachricht empfangen:", nachricht, parameter)
            return (nachricht, parameter)
        except socket.timeout:
            print("Der Server", self.kommunikator.server_adresse(), "reagiert nicht. Bot wird beendet.")
            sys.exit()

    def starte(self, name):
        self.name = name
        self.schicke_nachricht(Nachrichten.ANMELDEN, [name])
        (antwort, parameter) = self.warte_auf_nachricht()
        if (antwort == Nachrichten.ANGEMELDET):
            self.starte_spiel()
        else:
            print("Ich konnte mich nicht registrieren.", "Grund: " + antwort + str(parameter))

    def schicke_nachricht(self, nachricht, parameter):
        print("Nachricht schicken:", nachricht, parameter)
        self.kommunikator.sende_nachricht(nachricht, parameter)

    def starte_spiel(self):
        while (True):
            nachricht, parameter = self.warte_auf_nachricht()
            if (nachricht == Nachrichten.NEUE_RUNDE):
                token = parameter[-1]
                self.schicke_nachricht(Nachrichten.ICH_MACHE_MIT, [token])
            else:
                self.reagiere_auf_nachricht(nachricht, parameter)

    def reagiere_auf_nachricht(self, kommando, parameter):
        pass

    def signal_handler(self, signal, frame):
        self.reagiere_auf_stopp()
        sys.exit()

    def reagiere_auf_stopp(self):
        self.schicke_nachricht(Nachrichten.ABMELDEN, [self.name])


class Nachrichten:
    ANMELDEN = "REGISTER"
    ANGEMELDET = "REGISTERED"
    NEUE_RUNDE = "ROUND STARTING"
    ICH_MACHE_MIT = "JOIN"
    DU_BIST_DRAN = "YOUR TURN"
    WUERFELN = "ROLL"
    GEWUERFELT = "ROLLED"
    ANSAGEN = "ANNOUNCE"
    SCHAUEN = "SEE"
    ABMELDEN = "UNREGISTER"
    SPIELER_WUERFELT = "PLAYER ROLLS"
    SPIELER_SAGT_AN ="ANNOUNCED"
    SPIELER_VERLIERT ="PLAYER LOST"
    SPIELSTAND = "SCORE"
