import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import hub_api

hub_api.hub_print("What is 2+2?", "blue")
text = hub_api.hub_input()
if text.strip() == "4":
    hub_api.hub_print("Correct!", "green")
else:    hub_api.hub_print("Incorrect. The answer is 4.", "red")