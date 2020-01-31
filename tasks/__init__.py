from invoke import Collection

from tasks import invites, repos

ns = Collection()
ns.add_collection(invites)
ns.add_collection(repos)
