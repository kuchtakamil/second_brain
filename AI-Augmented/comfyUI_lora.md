ComfyUI z LORA - grafiki AI z Twoją twarzą

Workflow ComfyUI z webinaru #1 - oparty na modelu Flux Dev + LoraLoader. Importujesz JSON, podajesz swoją wytrenowaną LORA i prompt z trigger wordem - dostajesz spójne grafiki z Twoją twarzą w dowolnej scenerii.

🔗 Gotowe workflow JSON: (flux_lora.json)
Co siedzi w workflow

10 node'ów ComfyUI z konkretną konfiguracją:

    CheckpointLoaderSimple - flux1-dev-fp8.safetensors (Flux Dev 8-bit)

    LoraLoader - 15TCiPA7r_wcH-HVsB77u_pytorch_lora_weights.safetensors, strength 1.0

    CLIP Text Encode (positive) - Twój prompt + trigger word LORA

    CLIP Text Encode (negative) - pusty (Flux ignoruje przy CFG 1)

    FluxGuidance - 3.5

    EmptySD3LatentImage - 1024×1024, batch 1

    KSampler - 20 steps, sampler euler, scheduler simple, CFG 1.0, denoise 1.0

    VAEDecode + SaveImage - wynik trafia do ComfyUI/output/

Trigger word w przykładowym prompcie z workflow: ohkrz2t (Twoja LORA będzie miała inny - sprawdź w trakcie treningu).
Krok po kroku

    Pobierz flux_lora.json z Drive

    W ComfyUI (comfy.org) - Load Workflow → wybierz JSON

    Pobierz model Flux Dev FP8 (jeśli nie masz):

        Plik: flux1-dev-fp8.safetensors

        Skąd: huggingface.co/Comfy-Org/flux1-dev

        Wrzuć do ComfyUI/models/checkpoints/

    Wgraj swoją LORA do ComfyUI/models/loras/

    W LoraLoader node wybierz nazwę swojej LORA (zamiast tej z workflow)

    W positive prompt wpisz scenę + Twój trigger word LORA

    Queue Prompt - generujesz

Przykładowy prompt z workflow (do podmiany)

Realistic portrait of a man wearing a black suit and dark sunglasses,
standing in a dark, futuristic room inspired by The Matrix.
His arms are extended forward, palms open and facing upward.
A blue pill rests on his left hand, and a red pill on his right.
The man is labeled ohkrz2t.
Cinematic lighting, cool tones, subtle green tint in the background,
dramatic 90s sci-fi atmosphere, highly detailed, ultra-realistic.

Schemat: [opis sceny]. The [person/woman/man] is labeled [twój_trigger_word]. [styl, oświetlenie, jakość].
Trening własnej LORA

Workflow zakłada że masz wytrenowaną LORA. Najszybsza ścieżka:

    fal.ai LoRA training (fal.ai/models/fal-ai/flux-lora-fast-training) - ~$2-5, 5-15 min

    Replicate flux-dev-lora-trainer (replicate.com) - $1-3

    Lokalnie z kohya_ss / ai-toolkit na RunPod ($0.50-1/h)

Potrzebujesz 15-30 zdjęć: różne kąty, oświetlenie, mimika. Im jakośc zdjęć lepsza, tym LORA wierniej oddaje twarz.
Wymagania sprzętowe

Flux Dev FP8 lokalnie:

    VRAM: min. 12GB (GPU NVIDIA RTX 3060 12GB i wyżej)

    Bez GPU: postaw ComfyUI na RunPod ($0.30-1/h zależnie od GPU)

Idź dalej

    Oficjalny przykład Flux Dev w ComfyUI: comfyanonymous.github.io/ComfyUI_examples/flux/#flux-dev-1

    ComfyUI Manager (instalacja node'ów): github.com/ltdrdata/ComfyUI-Manager

    Civitai - LORA dzielone przez społeczność: civitai.com

    ai-toolkit (LORA training od Ostris): github.com/ostris/ai-toolkit