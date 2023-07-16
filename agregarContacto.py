import xmpp

def agregarContacto(usuario, password, contacto):
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()
    if cli.auth(jid.getNode(), password, resource=jid.getResource()):
        cli.send(xmpp.Presence(to=contacto, typ='subscribe'))
        return True
    else:
        return False
