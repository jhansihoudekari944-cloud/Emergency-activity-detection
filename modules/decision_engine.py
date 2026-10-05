class DecisionEngine:

    def evaluate(self, fall, moving, sos, fire=False):

        score = 0

        if fall:
            score += 50

        if sos:
            score += 80

        if fire:
            score += 100

        if not moving:
            score += 20

        emergency = fall or sos or fire

        return emergency, score