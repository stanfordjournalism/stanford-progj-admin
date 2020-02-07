from invoke import Collection

from tasks import canvas, invites, repos

ns = Collection()
ns.add_collection(canvas)
ns.add_collection(invites)
ns.add_collection(repos)
