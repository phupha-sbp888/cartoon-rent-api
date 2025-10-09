"""Access policy for book service CRUD APIs."""

from rental_management.access_policies.global_api_access_policy import GlobalApiAccessPolicy


class BookApiAccessPolicy(GlobalApiAccessPolicy):
    """Access policy for book service CRUD APIs."""

    statements = [
        {"action": ["retrieve", "list"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "authenticated", "effect": "allow", "condition": "has_role_permission"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]
