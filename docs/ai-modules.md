<!-- {"notolog.app": {"created": "2026-01-24 00:00:00.000000", "updated": "2026-01-24 00:00:00.000000"}} -->
# AI Modules

Notolog Editor integrates three AI inference modules for the AI Assistant feature. Each module supports different backends and use cases.

## Overview

| Module | Backend | Use Case | Model Format |
|--------|---------|----------|--------------|
| **OpenAI API** | Cloud API | Cloud-based inference | N/A (API) |
| **On Device LLM** | ONNX Runtime GenAI | Local inference with hardware acceleration | ONNX |
| **Module llama.cpp** | llama-cpp-python | Local inference with GGUF models | GGUF |

---

## 1. OpenAI API Module

### Description
The OpenAI API module enables cloud-based inference using OpenAI's language models (GPT-4o, GPT-5.2, etc.) or any OpenAI-compatible API endpoint.

### Requirements
- OpenAI API key
- Internet connection
- Optional: Custom API endpoint for compatible services (Azure OpenAI, LocalAI, etc.)

### Configuration Settings (UI Labels)
| UI Label | Description                                   |
|----------|-----------------------------------------------|
| **API URL** | API endpoint URL                              |
| **API Key** | Your OpenAI API key (stored encrypted)        |
| **Supported Models** | Model name dropdown (e.g., `gpt-4o`, `gpt-5`) |
| **System Prompt** | Initial instructions for the model            |
| **Temperature** | Controls response randomness (0-100)          |
| **Maximum Response Tokens** | Maximum response length                       |
| **Prompt History Size** | Number of conversation turns to retain        |

### Pros & Cons
| Pros | Cons |
|------|------|
| Most capable models | Requires internet |
| No local hardware requirements | API costs |
| Easy setup | Data sent to cloud |

---

## 2. On Device LLM Module (ONNX)

### Description
The On Device LLM module uses [ONNX Runtime GenAI](https://github.com/microsoft/onnxruntime-genai){:target="_blank"} for local inference with hardware acceleration support.

### Requirements
- Python 3.10-3.13
- ONNX model files
- Package: `onnxruntime-genai` (included with Notolog)

### Supported Models
Download ONNX-optimized models from:
- [Hugging Face ONNX Models](https://huggingface.co/models?library=onnx){:target="_blank"}
- [Microsoft Phi-3 ONNX](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-onnx){:target="_blank"}

Model directories should contain `.onnx` files and configuration.

### Configuration Settings (UI Labels)
| UI Label | Description |
|----------|-------------|
| **ONNX Model Location** | Directory containing ONNX model files |
| **Temperature** | Controls response randomness (0-100, displayed as 0.0-1.0) |
| **Maximum Response Tokens** | Maximum response length (0 = unlimited) |
| **Hardware Acceleration** | Execution provider selection |
| **Prompt History Size** | Number of conversation turns to retain |

### Hardware Acceleration Providers

| Provider | Platform | Hardware Required | Package |
|----------|----------|-------------------|---------|
| **CPU (Default)** | All | Any CPU | `onnxruntime-genai` |
| **CUDA** | Linux/Windows | NVIDIA GPU + CUDA + cuDNN | `onnxruntime-genai-cuda` |
| **DirectML** | Windows | DirectX 12 GPU | `onnxruntime-genai-directml` |
| **OpenVINO** | Windows/Linux | Intel CPU/GPU/VPU | `onnxruntime-genai` |
| **CoreML** | macOS | Apple Silicon/Neural Engine | `onnxruntime-genai` |
| **TensorRT RTX** | Windows/Linux | NVIDIA RTX GPU | `onnxruntime-genai` |
| **QNN** | Linux | Qualcomm Snapdragon NPU | `onnxruntime-genai` |
| **MIGraphX** | Linux | AMD GPU with ROCm | `onnxruntime-genai` |

#### Provider Details

##### CPU (Default)
- **Hardware**: Any x86_64 or ARM64 CPU
- **Performance**: Baseline, no acceleration
- **Use Case**: Universal fallback, development

##### CUDA (NVIDIA GPUs)
- **Hardware**: NVIDIA GPU with sufficient VRAM
- **Requirements**:
  - CUDA Toolkit
  - cuDNN library
  - NVIDIA drivers
- **Install on Ubuntu 24.04+**:
  ```bash
  sudo apt install nvidia-cuda-toolkit nvidia-cudnn
  ```
- **Install package**: `pip install onnxruntime-genai-cuda` (replaces base package)
- **Model Selection**: Use CUDA-optimized models (look for `cuda` in model directory name)
- **Use Case**: NVIDIA GPU users on Linux/Windows

**Important**: Choose models that fit your GPU memory:
- **Phi-3-mini** (~4GB VRAM) - Good for most GPUs
- **Phi-3-medium** (~14GB VRAM) - Requires high-end GPU

##### DirectML (Windows)
- **Hardware**: Any DirectX 12 compatible GPU (NVIDIA, AMD, Intel)
- **Performance**: Good GPU acceleration on Windows
- **Use Case**: Windows users with modern GPUs
- **Install**: `pip install onnxruntime-genai-directml` (replaces base package)

##### OpenVINO (Intel)
- **Hardware**: Intel CPUs (with AVX2/AVX-512), Intel GPUs (Iris, Arc), Intel VPUs
- **Performance**: Optimized for Intel hardware
- **Use Case**: Intel-based systems

##### CoreML (Apple)
- **Hardware**: Apple Silicon (M1/M2/M3/M4), Neural Engine
- **Performance**: Optimized for Apple hardware
- **Use Case**: macOS on Apple Silicon

##### TensorRT RTX (NVIDIA)
- **Hardware**: NVIDIA RTX 20/30/40 series GPUs
- **Performance**: Highly optimized for NVIDIA RTX GPUs
- **Use Case**: NVIDIA RTX GPU users

##### QNN (Qualcomm)
- **Hardware**: Qualcomm Snapdragon with NPU (AI Engine)
- **Performance**: Optimized for Snapdragon AI accelerators
- **Use Case**: Qualcomm-based devices

##### MIGraphX (AMD)
- **Hardware**: AMD GPUs with ROCm support
- **Performance**: Optimized for AMD GPUs
- **Use Case**: AMD GPU users on Linux

### Model Selection Tips
- **CPU models**: Look for `cpu-int4` in model name (e.g., `Phi-3-mini-4k-instruct-onnx/cpu-int4-rtn-block-32`)
- **CUDA/GPU models**: Look for `cuda` in directory name (e.g., `Phi-3-mini-4k-instruct-onnx-cuda/cuda-int4-rtn-block-32`)
- **Model size matters**: Phi-3-mini (~2GB) vs Phi-3-medium (~9GB) - choose based on your GPU VRAM

### Pros & Cons
| Pros | Cons |
|------|------|
| Local/private inference | Model download required |
| Hardware acceleration | Limited model availability |
| No API costs | Hardware-dependent performance |
| Works offline | Provider compatibility varies |

---

## 3. Module llama.cpp (GGUF)

### Description
The Module llama.cpp uses [llama-cpp-python](https://github.com/abetlen/llama-cpp-python){:target="_blank"} for local inference with GGUF format models.

### Requirements
- Python 3.10-3.13
- GGUF model file
- Package: `llama-cpp-python` (optional extra)

### Installation
```bash
# Install with llama.cpp support
pip install notolog[llama]

# Or install separately
pip install llama-cpp-python
```

### Supported Models
GGUF models from:
- [Hugging Face GGUF Models](https://huggingface.co/models?library=gguf){:target="_blank"}
- [TheBloke's Collection](https://huggingface.co/TheBloke){:target="_blank"} (historic archive, 2,000+ models)

Popular models:
- Llama 2/3
- Mistral
- Phi-2/3
- Gemma
- Qwen

### Configuration Settings (UI Labels)
| UI Label | Description |
|----------|-------------|
| **Model Location** | Path to `.gguf` file |
| **Context Window Size** | Maximum context size (default: 2048) |
| **Chat Formats** | Model-specific chat template dropdown |
| **System Prompt** | Custom system instructions |
| **Response Temperature** | Controls response randomness (0-100) |
| **Max Tokens per Response** | Maximum response length (0 = context window limit) |
| **Size of the Prompt History** | Conversation history limit |

### Chat Formats
| Format | Models |
|--------|--------|
| `auto` | Auto-detect from model metadata |
| `chatml` | Mistral, Qwen, many others |
| `llama-2` | Llama 2 models |
| `llama-3` | Llama 3 models |
| `gemma` | Google Gemma |
| `phi-3` | Microsoft Phi-3 |

### Performance Tips
- The module automatically uses all CPU cores
- Quantized models (Q4_K_M, Q5_K_M) offer good quality/speed balance
- Larger context windows require more memory

### Pros & Cons
| Pros | Cons |
|------|------|
| Wide model compatibility | CPU-only (in this integration) |
| Large model ecosystem | May be slower than GPU |
| Works offline | Model file required |
| No API costs | Memory-intensive for large models |

---

## Comparison

### Performance (Relative)

| Module | Speed | Quality | Privacy | Ease of Setup |
|--------|-------|---------|---------|---------------|
| OpenAI API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| On Device LLM (GPU) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| On Device LLM (CPU) | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Module llama.cpp | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### Recommendations

| Use Case | Recommended Module |
|----------|-------------------|
| Best quality, no hardware limits | OpenAI API |
| Privacy-focused, have NVIDIA GPU | On Device LLM + CUDA |
| Privacy-focused, Windows GPU | On Device LLM + DirectML |
| Privacy-focused, Apple Silicon | On Device LLM + CoreML |
| Privacy-focused, Intel CPU | On Device LLM + OpenVINO |
| Wide model choice, privacy | Module llama.cpp |
| Offline work required | On Device LLM or Module llama.cpp |

---

## Troubleshooting

### On Device LLM Common Issues

**Error: "Unknown provider name 'X'"**
- The provider is not supported in your onnxruntime-genai build
- Solution: Use CPU or install the correct package variant

**Error: "CUDA execution provider is not enabled"**
- CUDA requires separate package
- Solution: `pip install onnxruntime-genai-cuda` (replaces base package)

**Error: "libcublasLt.so.12: cannot open shared object file"** or **"libcudnn.so.9: cannot open shared object file"**
- CUDA runtime libraries not installed
- Solution (Ubuntu 24.04+):
  ```bash
  sudo apt install nvidia-cuda-toolkit nvidia-cudnn
  ```

**Error: "Failed to allocate memory for requested buffer"**
- GPU doesn't have enough VRAM for the model
- Solutions:
  1. Use a smaller model (e.g., Phi-3-mini instead of Phi-3-medium)
  2. Close other GPU applications
  3. Use CPU provider instead

**Error: "Model not found"**
- Model directory doesn't contain `.onnx` files
- Solution: Verify the path points to a directory with ONNX model files

### Module llama.cpp Common Issues

**Error: "Model not found"**
- File path is incorrect or file doesn't exist
- Solution: Use full path to the `.gguf` file

**Slow performance**
- Context window too large
- Solution: Reduce Context Window Size in settings

**Out of memory**
- Model too large for available RAM
- Solution: Use a smaller/more quantized model (e.g., Q4_K_M)

---

## Package Installation Summary

### Base Installation
```bash
pip install notolog
```
Includes: `onnxruntime-genai` (CPU)

### Optional Extras
```bash
# llama.cpp support
pip install notolog[llama]
```

### GPU Acceleration (Manual)
```bash
# NVIDIA CUDA (Linux/Windows) - replaces base onnxruntime-genai
pip uninstall onnxruntime-genai
pip install onnxruntime-genai-cuda

# DirectML (Windows) - replaces base onnxruntime-genai
pip uninstall onnxruntime-genai
pip install onnxruntime-genai-directml

# To switch back to CPU-only (use --force-reinstall to ensure clean install)
pip uninstall onnxruntime-genai-cuda  # or -directml
pip install --force-reinstall onnxruntime-genai
```

**Important Notes**:
- CUDA, DirectML, and base packages all provide the same `onnxruntime_genai` Python module
- They **cannot** be installed together - the last installed package wins
- If you uninstall the GPU package, use `--force-reinstall` when reinstalling the base package
- After changing packages, restart the application

