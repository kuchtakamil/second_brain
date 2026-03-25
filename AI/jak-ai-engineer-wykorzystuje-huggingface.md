# Jak AI Engineer może wykorzystać ekosystem Hugging Face

Poniżej zestawienie możliwości wykorzystania Hugging Face, uporządkowane od najważniejszych z perspektywy codziennej pracy AI Engineera:

1. **Hugging Face Hub (Modele)** - Wyszukiwanie, pobieranie i udostępnianie wariantów modeli open-source/open-weights (np. *Llama, Mistral, BERT*). Służy jako branżowy "GitHub dla modeli AI".
2. **Biblioteka `transformers`** - Standardowy framework do pobierania konfiguracji, inicjalizacji, fine-tuningu i inferencji modeli opartych na architekturze Transformer.
3. **Hugging Face Datasets (Hub i biblioteka)** - Wyszukiwanie gotowych zbiorów danych do treningu/ewaluacji. Biblioteka pozwala na ich niezwykle wydajne przetwarzanie (np. stronicowanie, streaming, mapowanie wielowątkowe bez zapychana pamięci RAM).
4. **PEFT (Parameter-Efficient Fine-Tuning) & LoRA** - Wykorzystywanie biblioteki PEFT do taniego i szybkiego dotrenowywania (fine-tuningu) gigantycznych modeli LLM na pojedynczych kartach graficznych dzięki mrożeniu bazowego modelu i aktualizacji tylko małych adaptatorów.
5. **Tokenizers** - Korzystanie z wysoce zoptymalizowanej (napisanej w języku Rust) biblioteki do błyskawicznej tokenizacji tekstu (czyli koniecznej konwersji tekstu na wektory/idki zrozumiałe dla sieci neuronowej).
6. **Polityka AutoClasses (`AutoModel`, `AutoTokenizer`)** - Pisanie generycznego kodu. Pozwala przekazać tylko stringa z nazwą modelu, a biblioteka sama pod maską doczytuje odpowiednią architekturę i konfigurację (abstrahowanie szczegółów modeli).
7. **Kwantyzacja (`bitsandbytes`, GPTQ, AWQ)** - Zmniejszanie wagi modeli (do 4-bit / 8-bit) we współpracy z ekosystemem HF. Umożliwia to zmieszczenie potężnych modeli w ograniczonej pamięci VRAM podczas inferencji czy trenowania z użyciem QLoRA.
8. **Text Generation Inference (TGI)** - Wdrażanie modeli LLM na produkcję (Deployment). TGI to napisany w Rust i Pythonie serwer gRPC/REST od HF ułatwiający wysokowydajną serwowanie z optymalizacją m.in. na niskie opóźnienia i Paged Attention (Continuous Batching).
9. **Pipelines** - Szybkie prototypowanie i testowanie modeli. API `pipeline` w kilku linijkach realizuje złożony workflow (preprocess + model pred + postprocess) dla danego zadania (np. *sentiment-analysis*).
10. **Hugging Face Spaces (Gradio / Streamlit)** - Szybkie i bezpłatne tworzenie, oraz hostowanie demonstracji aplikacji AI (Proof of Concept) za pomocą łatwych interfejsów webowych, by zademonstrować efekty klientom lub zespołowi.
11. **Hugging Face Accelerate** - Konfigurowanie elastycznego skalowania treningu – biblioteka oddziela logikę PyTorch od logiki wielo-procesowej. Pozwala przenieść kod trenowania z jednego GPU na wielkie klastry (Multi-GPU, TPU) przy minimalnych zmianach w skrypcie bazowym.
12. **TRL (Transformer Reinforcement Learning)** - Używanie zaawansowanej biblioteki do dostrajania (alignmentu) LLM-ów pod preferencje człowieka z użyciem RLHF, DPO, PPO, żeby modele bardziej odpowiadały na instrukcje chatowe.
13. **Format Safetensors** - Stosowanie wysoce bezpiecznego i szybkiego formatu ładowania wag (`.safetensors`). AI Engineer wybiera go zamiast Pickle/bin, chroniąc serwery przed złośłiwym kodem podczas doczytywania wag "z internetu".
14. **Biblioteka `evaluate`** - Używanie ustandaryzowanego interfejsu (na np. HF Evaluate) do obliczania specyficznych dla AI miar testowych (BLEU, ROUGE, Exact Match, wer) by oszacować dokładność nowego modelu.
15. **Hugging Face Optimum** - Skupienie na ekstremalnej wydajności - optymalizowanie modeli pod konkretny sprzęt (np. Intel, AWS Inferentia) lub konwertowanie do ONNX (ONNX Runtime) i tensorRT by wyciągnąć maksimum z hardware'u na produkcji.
16. **Inference Endpoints** - Bezserwerowe (lub dedykowane) skalowanie modeli. Uruchamianie wybranych modeli z Hub'a jako endpointów API kliknięciem z poziomu płatnego planu chmury.
17. **Biblioteka `diffusers`** - Działanie na innej gałęzi GenAI - praca specjalnie pod modele dyfuzyjne (np. z rodziny *Stable Diffusion*), by inżynieryjnie generować i integrować obrazy czy audio.
18. **GGUF i lokalna inferencja** - Obecnie HF Hub idealnie integruje sie z `llama.cpp`. AI Engineer pobiera z Hub'a skwantowane pliki GGUF i potrafi odpalić model LLM bezpośrednio na lokalnym procesorze (CPU maszyn dev) czy Mac'u (Metal).
19. **Hugging Face Agents / smolagents** - Tworzenie zintegrowanych systemów "Agents", w których potężny LLM dostaje zestaw przygotowanych przez inżyniera narzędzi Pythona (Tool calling) by sam realizował wieloetapowe operacje zewnętrzne. 
20. **Timm (PyTorch Image Models)** - Inżynieria w Computer Vision - sięganie po potężny zbiór bardzo wydajnych implementacji sieci na obrazie (jak np. ResNet, ViT), natywnie wpleciony dziś w Hub HF.
