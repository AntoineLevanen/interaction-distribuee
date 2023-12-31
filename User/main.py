#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  User version 1.0
#  Created by Ingenuity i/o on 2023/11/18
#

import sys
import threading
import ingescape as igs
import qtmodern
from PyQt5.QtWidgets import QApplication
from qtmodern import styles

import UI


def input_callback(msg_type, msg):
    """
    sending user message to main_agent
    msg : string formated like this "hour # user name # message" 
    """
    # arguments_list = (str(" "), msg) # str type to represent a message
    arguments_list = (msg_type, msg) # str type to represent a message
    igs.service_call("main_agent", "waitMessage", arguments_list, "")



def start_UI(input_callback):
    """exection de l'interface utilisateur"""
    app = QApplication(sys.argv)                            # nouvelle application PyQt5
    styles.dark(app)                                        # thème sombre de l'interface user
    window = UI.UserWindow(
        callback_message=input_callback)           # instance de UI User window définie dans le fichier associé
    qtmodern.styles.dark(app)                               # Style 'Modern' sur l'interface
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()                                               # affichage de l'application
    app.exec_()                                             # gestion de l'executuion et de la fermeture...
    app.exit()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    # Nouveau thread pour démarrer l'interface graphique de l'agent sans bloquer le déroulement du main 
    thread_UI = threading.Thread(target=start_UI, args=(input_callback,))
    thread_UI.start()


    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.definition_set_description("""Un utilisateur et son interface.""")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    # thread_UI.join() # wait for process to finish
    igs.stop()