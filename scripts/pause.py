class Pause(object):
    def __init__(self, paused=False):
        self.pausado = paused
        self.timer = 0
        self.tempo_pausa = None
        self.func = None
        
    def update(self, dt):
        if self.tempo_pausa is not None:
            self.timer += dt
            if self.timer >= self.tempo_pausa:
                self.timer = 0
                self.pausado = False
                self.tempo_pausa = None
                return self.func
        return None

    def pausar(self, tempo_pausa=None, func=None):
        self.timer = 0
        self.func = func
        self.tempo_pausa = tempo_pausa
        self.flip()

    def flip(self):
        self.pausado = not self.pausado