"""Simple IT helpdesk ticket system."""
import json
import os
import platform
import re
import subprocess  # nosec B404
from datetime import datetime

# Global state
tickets = {}
TICKET_COUNTER = 100
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a new ticket and return its number."""
    global TICKET_COUNTER  # pylint: disable=global-statement
    if audit_trail is None:
        audit_trail = []
    priority = int(urgency)
    if not 1 <= priority <= 5:
        raise ValueError(f"Urgency must be between 1 and 5, got {priority}")
    TICKET_COUNTER += 1
    tickets[TICKET_COUNTER] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }
    audit_trail.append(
        f"{user} raised #{TICKET_COUNTER} at {datetime.now()}"
    )
    return TICKET_COUNTER


def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to a ticket."""
    try:
        tickets[ticket_id]["notes"].append(note)
    except KeyError:
        print("Cannot add note: ticket", ticket_id, "does not exist")


def close_ticket(ticket_id, password):
    """Close a ticket if the admin password is correct."""
    if ADMIN_PASSWORD and password == ADMIN_PASSWORD:
        del tickets[ticket_id]


def unresolved_high_priority():
    """Return ids of high priority tickets with no technician."""
    result = []
    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= 4 and ticket["tech"] is None:
            result.append(ticket_id)
    return result


def ping_user_machine(hostname):
    """Ping a machine by hostname."""
    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname):
        raise ValueError("Invalid hostname")
    count_flag = "-n" if platform.system() == "Windows" else "-c"
    return subprocess.call(  # nosec B603 B607
        ["ping", count_flag, "1", hostname]
    )


def save_tickets(file="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(tickets))


def main():
    """Run the demo."""
    t1 = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    try:
        raise_ticket("joe", "vpn", "-7")
    except ValueError as err:
        print("Ticket rejected:", err)
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    level = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ) or "3"
    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as err:
        print("Ticket rejected:", err)
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
