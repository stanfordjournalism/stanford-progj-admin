from invoke import Collection

from tasks import invites

ns = Collection()
ns.add_collection(invites)
