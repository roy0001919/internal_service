from .resources import api_bp
from flask_restful import Resource, Api

api = Api(api_bp)

from .resources.tab_coform import COform, COformSearchOpen
api.add_resource(COform, '/coform')
api.add_resource(COformSearchOpen, '/coform/searchopen')
# PUT/DELETE/GET, id is required for the endpoint.
# POST request id is not allowed. for querying purposes

from .resources.tab_dailyopt import DailyOPT, DailyOPTLastTen
api.add_resource(DailyOPT, '/dailyopt')
api.add_resource(DailyOPTLastTen, '/dailyopt/lastten')
# PUT/DELETE/GET, id is required for the endpoint.
# POST request id is not allowed. for querying purposes

from .resources.tab_cashpymt import Cashpymt, cashPymtSend
api.add_resource(Cashpymt, '/cashpymt')
api.add_resource(cashPymtSend, '/cashpymtsend')

# PUT/DELETE/GET, id is required for the endpoint.
# POST request id is not allowed. for querying purposes

from .resources.tab_search import SearchCashPymt, SearchMailOrder, ExportCsv, SearchMailOrderUpdate, SearchCashDelete
api.add_resource(SearchCashPymt, '/search/cashpymt')
api.add_resource(SearchCashDelete, '/search/cashpymt/delete/<string:id>/<string:tab>')
api.add_resource(SearchMailOrder, '/search/mailorder')
api.add_resource(SearchMailOrderUpdate, '/search/mailorder/update')
api.add_resource(ExportCsv, '/exportcsv')
# api.add_resource(PymtUnrec, '/pymtunrec')


from .resources.tab_modify import COformMods
api.add_resource(COformMods, '/modify/coform')


# POST_only

from .resources.tab_user import Login
api.add_resource(Login, '/login')


from .resources.tab_auth_user import AuthUser
api.add_resource(AuthUser, '/authuser')