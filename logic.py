def calculate_split(amount, people, tip_percent, special_person_percent=None):
    """
    Beräkna totalbelopp med dricks och belopp per person.

    Args:
        amount: Totalbeloppet (float).
        people: Antal personer (int).
        tip_percent: Dricksprocent (float).
        special_person_percent: Procentandel som en specifik person betalar
                                av totalbeloppet med dricks (float eller None).

    Returns:
        Dictionary med:
            - 'total_med_dricks': Totalt belopp med dricks.
            - 'special_person_share': Belopp för specialpersonen (om angivet).
            - 'others_share': Belopp per övrig person (om angivet).
            - 'per_person': Belopp per person vid jämn delning (om ingen specialprocent).

    Raises:
        ValueError: Om people <= 0, eller om special_person_percent används
                    med people <= 1.
    """
    if people <= 0:
        raise ValueError("Antal personer måste vara större än 0.")

    if special_person_percent is not None:
        if people <= 1:
            raise ValueError(
                "Specialprocent kräver minst 2 personer."
            )
        if not (0 <= special_person_percent <= 100):
            raise ValueError(
                "Specialprocent måste vara mellan 0 och 100."
            )

    total_med_dricks = amount * (1 + tip_percent / 100)

    if special_person_percent is not None:
        special_person_share = total_med_dricks * (special_person_percent / 100)
        resterande = total_med_dricks - special_person_share
        others_share = resterande / (people - 1)
        return {
            "total_med_dricks": total_med_dricks,
            "special_person_share": special_person_share,
            "others_share": others_share,
            "per_person": None,
        }

    per_person = total_med_dricks / people
    return {
        "total_med_dricks": total_med_dricks,
        "special_person_share": None,
        "others_share": None,
        "per_person": per_person,
    }
