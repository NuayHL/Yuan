import time

class Timer:
    def __init__(self, avg_count_lenth:int = 0):
        self.reset()
        self._use_lenth_avg = False

        if avg_count_lenth != 0:
            assert avg_count_lenth > 0 and avg_count_lenth != 1
            self._use_lenth_avg = True
            self._count_lenth = avg_count_lenth
            self._time_period_list = [0.0] * self._count_lenth
            self._idx = 0

    def reset(self):
        self._total_time = 0.0
        self._counts = 0
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):
        self._period = time.perf_counter() - self._start_time

        if self._use_lenth_avg:
            self._time_period_list[self._idx] = self._period
            self._idx += 1
            self._idx %= self._count_lenth

        self._total_time += self._period
        self._counts += 1
        self._start_time = None
        return self._period

    def tick(self):
        current_time = time.perf_counter()
        self._period = current_time - self._start_time

        if self._use_lenth_avg:
            self._time_period_list[self._idx] = self._period
            self._idx += 1
            self._idx %= self._count_lenth

        self._total_time += self._period
        self._counts += 1
        self._start_time = current_time
        return self._period

    def up2now(self):
        return time.perf_counter() - self._start_time

    def is_paused(self):
        return self._start_time is None

    def average_time(self):
        assert self._counts > 0
        return self._total_time/self._counts

    def average_time_in_lenth(self, lenth=None):
        assert self._use_lenth_avg
        if lenth is None:
            return sum(self._time_period_list) / min(self._count_lenth, self._counts)
        else:
            assert lenth <= self._count_lenth
            return sum(self._time_period_list[self._idx - lenth : self._idx]) / min(lenth, self._counts)

    def total_time(self):
        return self._total_time

    @staticmethod
    def period2str(seconds):
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

    @staticmethod
    def period2list(seconds):
        fin = [0.0, 0.0, 0.0]
        if seconds > 3600:
            hours = seconds//3600
            fin[0] = hours
            seconds %= 3600
            mins = seconds // 60
            fin[1] = mins
        elif seconds > 60:
            mins = seconds // 60
            fin[1] = mins
            seconds %= 60
        fin[2] = seconds
        return fin
