from subprocess import run, Popen, PIPE
from api_requester import ApiRequester
import re

api_req = ApiRequester()

# Some utils.
rofi_command = ['rofi', '-dmenu', '-lines', '10', '-dynamic', 'true', '-i', '-p', 'define:']
pattern = re.compile(r"(\d+):")

# Get query from user.
result = run(rofi_command, capture_output=True, text=True)
query = result.stdout.strip()

# Get data from API.
api_req.query(query)

# Show sense categories to user.
preview = api_req.get_results_preview()
preview = [f"{idx}: {p['text']}" for idx, p in enumerate(preview)]
rofi_input = "\n".join(preview)

# Allow user to pick sense categories and view definitions.
while True:
    # Get sense category.
    echo = Popen(["echo", rofi_input], stdout=PIPE)
    result = run(rofi_command + ['-no-custom'], stdin=echo.stdout, capture_output=True, text=True)

    # Get the user's category choice.
    if match := pattern.match(result.stdout):
        idx = int(match.group(1))
        definitions = api_req.get_senses_definitions(idx)['definitions']
        definitions_input = "\n".join(definitions)
        definitions_input = "⬅ Go back.\n" + definitions_input

        # Display definitions
        echo = Popen(["echo", definitions_input], stdout=PIPE)
        result = run(rofi_command + ['-no-custom'], stdin=echo.stdout, capture_output=True, text=True)

        # Break if user does not choose to go back.
        if not result.stdout.startswith("⬅"):
            break
 
echo.stdout.close()
