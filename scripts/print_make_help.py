import re
import sys

BOLD = "\033[1m"
BLUE = "\033[94m"
END = "\033[0m"

print("Usage: make <target>\n")
print(BOLD + "%-20s%s" % ("target", "description") + END)
for line in sys.stdin:
    match = re.match(r"^([a-zA-Z0-9_/\\-]+\.?.*?):.*?## (.*)$$", line)
    if match:
        target, help = match.groups()
        print(BLUE + "%-20s" % (target) + END + "%s" % (help))
