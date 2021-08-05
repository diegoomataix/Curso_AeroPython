def exam_norms(dur, breakk):
    """Comprueba si un examen cumple la normativa de la UPM.

    """
    if dur <= 3:
        return True
    else:
        #if descanso:
        #    return True
        #else:
        #    return False
        return breakk  # ¡Equivalente!

if not exam_norms(5, breakk=False):
    print("Review exam conditions!")

# print(exam_norms(2, False))
