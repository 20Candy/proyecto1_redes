import xmpp

def iniciar_sesion(usuario, password):
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    if cli.connect() != "":
        if cli.auth(jid.getNode(), password, "myclient"):
            cli.sendInitPresence()
            return cli
    return None
