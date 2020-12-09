from subprocess import run, Popen, PIPE
from api_requester import ApiRequester

api_req = ApiRequester()

api_req.query('set')

print(api_req.get_results_preview())
print(api_req.get_senses_definitions(1, 5))
