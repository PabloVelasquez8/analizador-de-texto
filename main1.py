from collections import Counter
def normalize_text(text: str) -> str:
    """
    Convierte a minúsculas,
    elimina puntuación común,
    elimina espacios extra.
    Mantiene letras y números.
    """
    if not isinstance(text, str):
        raise TypeError("El texto debe ser un string.")

    text = text.lower()

    # Mantener solo letras, números y espacios
    text = "".join(c for c in text if c.isalnum() or c.isspace())

    # Eliminar espacios extra
    return " ".join(text.split())

def tokenize(text: str) -> list[str]:
    return text.split()

class TextAnalyzer:
    def __init__(self, text: str):
        if not text.strip():
            raise ValueError("El texto no puede estar vacío.")

        self.original_text = text
        self.normalized_text = ""
        self.tokens = []
        self.counts = Counter()
        self.unique_tokens = set()

    def analyze(self):
        self.normalized_text = normalize_text(self.original_text)
        self.tokens = tokenize(self.normalized_text)

        self.counts = Counter(self.tokens)
        self.unique_tokens = set(self.tokens)

    def report(self):
        if not self.tokens:
            print("No hay datos para analizar.")
            return

        total = len(self.tokens)
        unique = len(self.unique_tokens)

        print("\n===== REPORTE =====")
        print(f"Total de tokens: {total}")
        print(f"Tokens únicos: {unique}")

        print("\nTop 10 tokens más frecuentes:")
        for token, count in self.counts.most_common(10):
            print(f"{token}: {count}")

        avg_length = sum(len(t) for t in self.tokens) / total
        print(f"\nLongitud promedio de palabra: {avg_length:.2f}")

        max_len = max(len(t) for t in self.tokens)
        min_len = min(len(t) for t in self.tokens)

        longest = [t for t in self.unique_tokens if len(t) == max_len]
        shortest = [t for t in self.unique_tokens if len(t) == min_len]

        print(f"\nPalabra(s) más larga(s): {longest}")
        print(f"Palabra(s) más corta(s): {shortest}")

    def query(self, word: str):
        word = normalize_text(word)

        if word not in self.counts:
            print("La palabra no aparece en el texto.")
            return

        frequency = self.counts[word]
        total = len(self.tokens)
        percentage = (frequency / total) * 100

        print(f"\nFrecuencia: {frequency}")
        print(f"Porcentaje: {percentage:.2f}%")

        if frequency == 1:
            print("Clasificación: rara")
        elif frequency >= 5:
            print("Clasificación: común")
        else:
            print("Clasificación: intermedia")

def read_from_file():
    path = input("Ingrese la ruta del archivo .txt: ")

    try:
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        if not text.strip():
            raise ValueError("El archivo está vacío.")

        return text

    except FileNotFoundError:
        print("Error: archivo no encontrado.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return None

def read_from_console():
    print("Pegue el texto. Escriba END en una línea para finalizar:")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    text = "\n".join(lines)

    if not text.strip():
        print("Error: texto vacío.")
        return None

    return text

def run_tests():
    print("Ejecutando pruebas...")

    # Prueba normalización
    assert normalize_text("Hola, Mundo!! Python 3.") == "hola mundo python 3"

    # Prueba tokenización
    assert tokenize("hola mundo") == ["hola", "mundo"]

    # Prueba conteo
    ta = TextAnalyzer("Hola hola mundo")
    ta.analyze()
    assert ta.counts["hola"] == 2
    assert ta.counts["mundo"] == 1

    print("Pruebas superadas.\n")

def main():
    run_tests()

    print("Seleccione modo:")
    print("1 - Leer desde archivo")
    print("2 - Ingresar texto en consola")

    option = input("Opción: ")

    if option == "1":
        text = read_from_file()
    elif option == "2":
        text = read_from_console()
    else:
        print("Opción inválida.")
        return

    if text is None:
        return

    try:
        analyzer = TextAnalyzer(text)
        analyzer.analyze()
        analyzer.report()

        while True:
            word = input("\nIngrese palabra para consultar (o 'exit' para salir): ")
            if word.lower() == "exit":
                break
            analyzer.query(word)

    except Exception as e:
        print(f"Error durante el análisis: {e}")


if __name__ == "__main__":
    main()
