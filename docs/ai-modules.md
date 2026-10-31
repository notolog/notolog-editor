# AI Modules

The AI Assistant supports three inference backends. Use the [AI Assistant Guide](ai-assistant.md)
for basic setup and the [Configuration Guide](configuration.md#ai-module-settings) for settings.

## Overview

| Module | Runs inference | Requires |
|--------|----------------|----------|
| OpenAI API | At the configured API endpoint | Compatible endpoint, model access, and credentials |
| On Device LLM | Locally through ONNX Runtime GenAI | Compatible ONNX GenAI model directory and runtime |
| Module llama.cpp | Locally through llama-cpp-python | Compatible GGUF model and runtime |

Model quality, speed, and memory requirements depend on the model, hardware, and runtime.
The backend name alone does not establish a quality or performance ranking.

## OpenAI API

Configure the API URL, API key, and supported model in **Settings → OpenAI API**.
Custom endpoints must support the request format used by Notolog; an arbitrary model API is not interchangeable.

Requests send the API key, prompt, configured system prompt, and included conversation history to
the selected endpoint. Use HTTPS for remote services and verify the destination before entering credentials.
The key is encrypted in local settings using an application key; this does not protect it from someone
who can access both the settings and the application key.

## On Device LLM (ONNX)

Base pip installations include the CPU `onnxruntime-genai` package. Conda packaging has a different
dependency set; a missing backend is not enabled merely by selecting it in Settings.

Models must be exported for the installed ONNX Runtime GenAI version. Select the directory containing
`genai_config.json` and all model/tokenizer files referenced by that configuration. Ordinary ONNX exports,
including models intended for transformers.js, are not automatically compatible.

### Hardware acceleration

| Provider | Setup |
|----------|-------|
| CPU | Use the base `onnxruntime-genai` package and a CPU-compatible model. |
| CUDA | Requires a compatible `onnxruntime-genai-cuda` build, NVIDIA drivers and runtime libraries, and a compatible model. |
| DirectML | Requires a compatible Windows `onnxruntime-genai-directml` build and model. |
| Other listed providers | Require explicit support in the installed GenAI build and model; the Settings list is not a list of bundled accelerators. |

See the [upstream GenAI installation guide](https://onnxruntime.ai/docs/genai/howto/install.html)
for supported packages and driver/runtime requirements. ONNX Runtime's provider catalog does not mean
every provider is available in ONNX Runtime GenAI's standard Python packages.

Other provider names describe possible runtime integration targets, not extra
accelerators installed by the base Notolog package:

| Provider family | Hardware ecosystem |
|-----------------|--------------------|
| OpenVINO | Intel processors and accelerators |
| CoreML | Apple platforms |
| TensorRT RTX | NVIDIA RTX GPUs |
| QNN | Qualcomm accelerators |
| MIGraphX | AMD GPUs |

Consult the [ONNX Runtime provider catalog](https://onnxruntime.ai/docs/execution-providers/)
and the selected GenAI build's documentation before choosing one. A provider in
ONNX Runtime, or a name exposed by Notolog, does not establish GenAI model support.

Install only one GenAI variant: CPU, CUDA, and DirectML share the same Python module.
Remove the existing variant before switching, and restart Notolog afterwards.
For Notolog 1.2.4 on Python 3.11–3.14, keep CPU and CUDA within
`>=0.18.0,<1.0.0`. DirectML uses a separate version line: `>=0.14.1,<0.15.0`.
The [DirectML 0.14.1 wheels](https://pypi.org/project/onnxruntime-genai-directml/0.14.1/#files)
target Windows x64. For every variant, verify that a wheel exists for your platform;
package availability alone does not guarantee that your model and driver are compatible.
After checking those prerequisites, switch an isolated pip environment to CUDA or
DirectML with the matching command pair:

```bash
# CUDA
pip uninstall onnxruntime-genai onnxruntime-genai-directml
pip install "onnxruntime-genai-cuda>=0.18.0,<1.0.0"

# DirectML on Windows
pip uninstall onnxruntime-genai onnxruntime-genai-cuda
pip install "onnxruntime-genai-directml>=0.14.1,<0.15.0"
```

Choose one pair. These are manual runtime substitutions; Notolog's base package
metadata still declares the CPU distribution. A later package upgrade can install
it again, so recheck the environment after dependency changes.
When returning to CPU, reinstall through Notolog so its package requirements apply:

```bash
pip uninstall onnxruntime-genai-cuda onnxruntime-genai-directml
pip install --upgrade notolog
```

If variants were installed together, shared files may have been overwritten or
removed. After uninstalling the GPU distributions, repair the CPU distribution
with `pip install --force-reinstall "onnxruntime-genai>=0.18.0,<1.0.0"`.
Keep it within the requirements of the installed Notolog release.

### Loading and memory

Loading time depends on model size, storage, and available memory.
Notolog attempts CPU fallback after provider initialization errors and can reduce generation length
after allocation failures. These fallbacks cannot make an incompatible model or insufficient RAM work.
Try a smaller model or lower the generation limit if problems persist.

## Module llama.cpp (GGUF)

For pip installations:

```bash
pip install "notolog[llama]"
```

A C++ compiler is needed when pip builds llama-cpp-python from source. Prebuilt distributions have
their own architecture and acceleration support. Follow the
[llama-cpp-python installation instructions](https://github.com/abetlen/llama-cpp-python#installation)
for the required backend.

Select the GGUF file in **Settings → Module llama.cpp** and choose its chat format:
`chatml` (the default), `llama-2`, or `gemma`. Match the format to the model card's chat template;
Notolog passes this selection to the runtime rather than detecting it automatically.
An arbitrary GGUF file is not necessarily a supported text-generation model.

Model collections such as [Qwen2 GGUF exports](https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF)
provide examples of quantized models. `Q4_K_M` and `Q5_K_M` are alternative
size/quality choices, not fixed memory requirements or guarantees of compatibility.
Use the model card, chat template, and installed runtime together when selecting a file.
For ONNX model directory examples, see [model setup](ai-assistant.md#on-device-llm-onnx).

### GPU layers

| Setting | Requested behavior |
|---------|--------------------|
| Auto | All layers on GPU for Apple Silicon; CPU on Intel Macs, Linux, and Windows |
| -1 | Offload all layers to an available supported GPU backend |
| 0 | CPU only |
| Positive number | Offload that many layers, subject to model and backend limits |

The setting requests offloading; the installed llama.cpp build must include the matching backend.
Apple Silicon needs a Metal-enabled build. If an Intel Mac hangs during loading, use **0** and retry.
Do not downgrade below Notolog's declared llama-cpp-python requirements.

Larger context windows increase memory use. Smaller quantized models can reduce resource requirements;
measure performance with your chosen model rather than relying on a generic token-rate estimate.

## Troubleshooting

| Problem | Action |
|---------|--------|
| Unknown ONNX provider | Select CPU or install a GenAI build that explicitly supports the provider. |
| Missing CUDA library | Check the required driver, CUDA, and cuDNN versions in the runtime's installation guide. |
| Missing `genai_config.json` | Select a complete GenAI model export, not a generic ONNX directory. |
| Model file not found | Check paths, permissions, and whether all download files are present. |
| Out of memory | Reduce model/context size and close other memory-intensive applications. |
| Chat-template markers in output | Check the model's tokenizer, chat template, and stop-token configuration. |
| API request fails | Check the endpoint, supported model, credentials, quota, and returned error. |

If zsh reports `no matches found: notolog[llama]`, quote the extra as above or
escape the brackets: `pip install notolog\[llama\]`.

A llama.cpp message such as `n_ctx_per_seq (2048) < n_ctx_train (...)` means the
configured context is smaller than the model's training context. It is not, by
itself, a load failure. Increasing the context can use more memory.
Likewise, a `skipping kernel_*_bf16` message identifies a skipped kernel; it does
not alone prove a fatal error or guarantee a working fallback. Read the subsequent
initialization result and follow the runtime's hardware requirements.

When reporting a problem, include Notolog, Python, runtime, OS, model, and provider versions.
Remove credentials and private document or conversation content from logs.
