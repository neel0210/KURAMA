# User IDs for each rank
RANKS = {
    "SAGE": [475193649],        # Sudo / Full Control
    "AKATSUKI": [],    # Sudo / Full Control
    "HOKAGE": [],      # High Priority
    "JONIN": [],       # Standard User
    "GENIN": []                # Restricted / New Users
}

def get_rank(user_id):
    for rank, ids in RANKS.items():
        if user_id in ids:
            return rank
    return "GENIN"

def is_sudo(user_id):
    rank = get_rank(user_id)
    return rank in ["SAGE", "AKATSUKI"]
