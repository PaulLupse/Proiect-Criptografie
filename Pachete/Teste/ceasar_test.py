from Pachete.Algoritmi.Basic import cezar

# Această porțiune de cod va pune cifrul lui Cezar sub o multitudine de teste pentru a verifica dacă codul este
# implementat fără erori

def over_26_shifts(multiple, positions ,message):

    # O buclă care validează un input din mulțimea {-1,1}
    # 1 este shift la dreapta
    # -1 este shift la stânga în alfabet

    while True:
        direction = int(input("Alegeti o directie (1 pentru dreapta -1 pentru stanga): "))
        if direction == 1:
            break
        elif direction == -1:
            break
        else:
            print("Alegeti o varianta din cele afisate")

    # Se definesc doua variabile care sunt egale cu valoarea initiala respectiv cu valoarea dupa inmultirea
    # variabilei positions cu un numar

    initial_value = cezar(message, direction * positions, "criptare")
    shift26 = direction * positions + (26 * multiple)
    shifted_value = cezar(message, shift26, "criptare")

    # Se verifică dacă cele doua variabile sunt egale

    if initial_value == shifted_value:
        return f"Valorile {initial_value} și {shifted_value} sunt egale"
    else:
        return "Eroare"

def main():
    print(over_26_shifts(2, 5, "taxi"))

if __name__ == "__main__":
    main()


