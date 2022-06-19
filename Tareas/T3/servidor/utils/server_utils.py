from threading import Thread, Event


class Timer(Thread):
    def __init__(self, duration=10, target=None, params=None):
        Thread.__init__(self)
        self.stop_event = Event()
        self.start_event = Event()
        self.duration = duration
        self.target = target
        self.params = params

        self.start()

    def stop(self):
        self.stop_event.set()

    def start_timer(self, duration=None, target=None, params=None):
        if target is not None:
            self.target = target
        if params is not None:
            self.params = params
        if duration is not None:
            self.duration = duration
        self.start_event.set()

    def run(self):
        while True:
            self.start_event.wait()
            self.start_event.clear()
            self.stop_event.clear()
            self.stop_event.wait(self.duration)
            if not self.stop_event.is_set():
                if callable(self.target):
                    if self.params:
                        self.target(*self.params)
                    else:
                        self.target()
                else:
                    raise Exception("Target function is not callable")
