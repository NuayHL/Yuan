import time

class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self._total_time = 0.0
        self._counts = 0
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):
        self._period = time.perf_counter() - self._start_time
        self._total_time += self._period
        self._counts += 1
        self._start_time = None
        return self._period

    def tick(self):
        current_time = time.perf_counter()
        self._period = current_time - self._start_time
        self._total_time += self._period
        self._counts += 1
        self._start_time = current_time
        return self._period

    def is_paused(self):
        return self._start_time is None

    def average_time(self):
        assert self._counts > 0
        return self._total_time/self._counts

    def total_time(self):
        return self._total_time

    @staticmethod
    def period_convert(seconds):
        fin = ''
        if seconds > 3600:
            hours = seconds//3600
            fin += '%dh ' % hours
            seconds %= 3600
            mins = seconds // 60
            fin += '%dm ' % mins
        elif seconds > 60:
            mins = seconds // 60
            fin += '%dm ' % mins
            seconds %= 60
        fin += '%.fs' % seconds
        return fin
