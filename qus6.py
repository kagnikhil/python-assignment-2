
import re
import sys
from collections import defaultdict, deque
from datetime import datetime

LOG_RE = re.compile(
    r"^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$"
)


def detect_suspicious(logs, x, t):
    failures = defaultdict(deque)
    failed_ips = defaultdict(deque)
    suspicious = {}

    for line in logs:
        match = LOG_RE.fullmatch(line.strip())
        if not match:
            continue

        timestamp, user, ip, status = match.groups()
        current = datetime.strptime(timestamp, "%H:%M")
        minute = current.hour * 60 + current.minute

        queue = failures[user]
        ips = failed_ips[user]

        while queue and minute - queue[0] > t:
            queue.popleft()
            ips.popleft()

        if status == "FAIL":
            queue.append(minute)
            ips.append(ip)

        elif len(queue) >= x and any(old_ip != ip for old_ip in ips):
            if user not in suspicious:
                suspicious[user] = timestamp

    return suspicious


def main():
    try:
        x, t = map(int, input().split())
        n = int(input())

        if not 1 <= x <= 100 or not 1 <= t <= 1440 or n < 0:
            print("Invalid input")
            return

        logs = [input() for _ in range(n)]
        result = detect_suspicious(logs, x, t)

        for user in sorted(result):
            print(user, result[user])

    except (ValueError, EOFError):
        print("Invalid input")


if __name__ == "__main__":
    main()
