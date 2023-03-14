import urllib.parse


def lid_ref(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + lid
            + "</a>"
        )
