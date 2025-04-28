import threading


class ParallelValue:
    """
    Parallel value. If running serially, use a single value. If running in parallel,
    use a value per thread.
    """

    def __init__(self, is_parallel, initial_value):
        """
        Constructor.

        :param is_parallel: Indicates if running in parallel.
        :param initial_value: The initial value.
        """
        self._is_parallel = is_parallel
        self._serial_value = initial_value
        self._parallel_values = threading.local()
        self._parallel_values.value = initial_value

    @property
    def value(self):
        """
        Get or set the value.
        """
        if self._is_parallel:
            return self._parallel_values.value
        else:
            return self._serial_value

    @value.setter
    def value(self, new_value):
        if self._is_parallel:
            self._parallel_values.value = new_value
        else:
            self._serial_value = new_value

    def __call__(self):
        """
        Convert to value type.
        """
        return self.value
