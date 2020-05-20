class ConfigReactor:
    """
    A configuration reactor is an object instance that handles changes to a predefined key. When a new value is
    detected, the react method is called, with a domain-specific implementation.
    """

    def react(self, val: str) -> None:
        raise NotImplementedError()
