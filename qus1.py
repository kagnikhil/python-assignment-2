
import re
import sys
from collections import defaultdict

EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9._+-])([A-Za-z0-9._+-]+@(?:[A-Za-z0-9-]+\.)+(?:com|edu|org))\b",
    re.IGNORECASE
)


def extract_emails(file_path):
    domains = defaultdict(set)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            for match in EMAIL_RE.finditer(line):
                email = match.group(1)
                username, domain = email.rsplit("@", 1)
                domains[domain.lower()].add(username.lower() + "@" + domain.lower())

    return domains


def main():
    file_path = input("Enter file path: ").strip()

    try:
        domains = extract_emails(file_path)

        for domain in sorted(domains):
            emails = domains[domain]
            print(domain, len(emails), min(emails))

    except (OSError, ValueError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
