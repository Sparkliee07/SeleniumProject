class AbortException(Exception):
    """
    Exception thrown when aborting a test.
    """

    def __init__(self):
        super().__init__("Test aborted.")
