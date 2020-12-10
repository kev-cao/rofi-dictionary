from subprocess import run, Popen, PIPE
from api_requester import ApiRequester
import re, json

def split_string(s, skip):
    """
    Splits a string with \n every skip characters. Will avoid breaking words.

    Parameters:
    s (String): The string to split.
    skip (Integer): How often to split in characters.

    Returns:
    String: The split string.
    """
    words = s.split()
    current_len = 0
    result = []

    for word in words:
        if current_len + len(word) > skip:
            result.append(f'\n{word}')
            current_len = len(word)
        else:
            result.append(f'{word}')
            current_len += len(word)

    return " ".join(result)

class RofiApp:
    def __init__(self):
        # Some utils.
        # States: ['EXIT', 'DEFINE', 'CATEGORIES', 'DEFINITIONS', 'DETAILED_DEF'] # self.state is the index in the above list.
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        self.state = 1
        self.rofi_command = ['rofi', '-dmenu', '-lines', '10', '-no-fixed-num-lines', '-i']
        self.pattern = re.compile(r"(\d+):")
        self.api_req = ApiRequester()

    def display_menu(self, menu, title, back_msg):
        """
        Displays a menu to the user.

        Parameters:
        menu (list): The menu list.
        title (String): The prompt title to show.
        back_msg (String): The message to show as the back entry.

        Return:
        Integer: The index of the menu option chosen, -1 if to go back, None if none chosen.
        """
        rofi_input = back_msg + "\n" + "\n".join(menu)
        echo = Popen(["echo", rofi_input], stdout=PIPE)
        result = run(self.rofi_command + ['-no-custom', '-p', title], stdin=echo.stdout, capture_output=True, text=True).stdout.strip()
        echo.stdout.close()

        if back_msg == result:
            return -1
        elif match := self.pattern.match(result):
            return int(match.group(1))
        else:
            return None

    def next_state(self, choice):
        """
        Updates the state from the current state and the user's choice.

        Parameters:
        choice (Integer): The index of the user's choice from the menu display.
        """
        if choice == None:
            # If the user escapes, then set state to EXIT.
            self.state = 0
        else:
            # Otherwise move state to the prev/next state.
            offset = -1 if choice == -1 else 1
            self.state += offset

    def run(self):
        """
        Runs the app until the user exits.
        """
        # These are used to remember the choices made in previous states when going back.
        defns_choice = defn_choice = 0 
        while self.state:
            if self.state == 1:
                # DEFINE State - Ask user for word.
                try:
                    result = run(self.rofi_command + ['-p', 'define:'], capture_output=True, text=True)
                    query = result.stdout.strip()
                    self.api_req.query(query)
                    choice = 1
                except KeyError:
                    if query != '':
                        echo = Popen(["echo", "ERROR: Word not found."], stdout=PIPE)
                        result = run(self.rofi_command + ['-only-match'], stdin=echo.stdout)
                        echo.stdout.close()
                    choice = -1

            elif self.state == 2:
                # CATEGORIES State - Show lexical categories of definitions.
                categories = self.api_req.get_results_preview()
                categories = [f"{idx}: {c['text']}" for idx, c in enumerate(categories)]
                choice = defns_choice = self.display_menu(categories, query, "⬅ Go back.")

            elif self.state == 3:
                # DEFINITIONS State - Show list of definitions.
                defns = self.api_req.get_senses_definitions(defns_choice, self.config['num_defns'])['definitions']
                fdefns = [f"{idx}: {d}" for idx, d in enumerate(defns)]
                choice = defn_choice = self.display_menu(fdefns, query, "⬅ Go back.")

            elif self.state == 4:
                # DETAILED_DEF State - Show a selected definition in the window.
                defn = defns[defn_choice]

                # Split defn every so many characters to make space.
                skip = self.config['chars_per_line']
                defn = split_string(defn, skip)

                choice = self.display_menu([defn], query,"⬅ Go back.")

            self.next_state(choice)


if __name__ == '__main__':
    app = RofiApp()
    app.run()
