import sched, time

class Target:
    def __init__(self, hour, minutes):
        self.hour = hour
        self.min = minutes


TARGETS = [Target(13, 24),Target(8, 0), Target(9, 0), Target(10, 0), Target(10, 30), Target(11, 0), Target(12, 0), Target(13, 0), Target(15, 0), Target(16, 0), Target(17, 0), Target(17, 30), Target(18, 30)]



class CardapioCache:
    cardapios = []
    scheduler = sched.scheduler(time.time, time.sleep)



    @staticmethod
    def should_update_cache():
        utc_time = time.gmtime()

        # TODO: considerar horario de verao depois

        current_hour = (24 + utc_time.tm_hour - 3) % 24  # UTC time menos 3 eh o horario de SP
        current_minute = utc_time.tm_min

        for t in TARGETS:
            if t.hour == current_hour and t.min == current_minute:
                return True

        return False
