import os
from google import genai
import json


def tag_with_llm(filename):
    # Start Gemini client
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise RuntimeError("Set GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=API_KEY)

    # Initialize prompt
    prompt1 = """Deluješ kot strokovni anotator besedil.
        Tvoja naloga je, da v spodnjem BESEDILU poiščeš pomembne besedilne odseke (span)
        in jih označiš s semantičnimi kategorijami.

        BESEDILO:
        "
    """

    prompt2 = """
    "

    OSNOVNE SEMANTIČNE OZNAKE:
    - definicija: del besedila, ki razlaga, kaj nek pojem pomeni.
    - primer: del besedila, ki podaja konkretno ilustracijo ali opis situacije.
    - egipt: del besedila, ki se nanaša na Egipt (zgodovina, ljudje, kraji, dogodki).

    DOVOLJENO:
    - Model lahko doda svoje nove oznake,
    vendar naj jih bo **zelo malo**.
    - Uporabljene oznake naj bodo **splošne**, **široko uporabne**
    in naj pomagajo pri **navigaciji po besedilu**.
    - Ne ustvarjaj preveč ozkih, specifičnih ali nepotrebnih oznak
    (npr. “zgodovinski_dogodek_iz_leta_1295”).
    - Nove oznake naj bodo kratke, jasne in opisne (npr. “pojem”, “lokacija”, “oseba”).

    IZHODNI FORMAT (strogo JSON):
    {
    "spansi": [
        {
        "oznaka": "<ime-oznake>",
        "besedilo": "<točen izsek iz besedila>",
        "zacetek": <indeks prvega znaka>,
        "konec": <indeks zadnjega znaka + 1>
        }
    ]
    }

    PRAVILA:
    1. Izseki morajo biti dobesedno prepisani iz originalnega besedila.
    2. Indeksi morajo ustrezati položajem v BESEDILU.
    3. Spansi se lahko prekrivajo.
    4. Uporabi čim manj različnih oznak, vendar naj bodo informativne.
    5. Vrni izključno veljaven JSON, brez dodatnih razlag ali komentarjev.
    """

    # Generate response for semantic tagging
    with open(filename, "r") as f:
        text = f.read()

        resp = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt1 + text + prompt2,
        )

    return json.loads(resp.text[8:-3])["spansi"]
