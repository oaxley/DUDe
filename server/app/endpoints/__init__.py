# imports all the blueprints from endpoints

from .company    import blueprint as BPCompany
from .unit       import blueprint as BPUnit
from .team       import blueprint as BPTeam
from .user       import blueprint as BPUser
from .right      import blueprint as BPRight
from .software   import blueprint as BPSoftware
from .user_right import blueprint as BPUserRight

routes = [
    BPCompany, BPUnit, BPTeam, BPUser,
    BPRight, BPSoftware, BPUserRight,
]
