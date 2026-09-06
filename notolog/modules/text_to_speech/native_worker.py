"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Native speech synthesis and PCM audio callbacks in an isolated worker.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""
import base64
import ctypes as c
import json
import os
import sys


class Model(c.Structure):
    _fields_ = [('size', c.c_size_t), ('magpie', c.c_char_p), ('codec', c.c_char_p),
                ('tokenizer', c.c_char_p), ('normalizer', c.c_char_p)]


class Runtime(c.Structure):
    # Layout from the pinned 0.1.0 tts.h; initialize through the library defaults.
    _fields_ = [('size', c.c_size_t)] + [(name, c.c_int32) for name in (
        'speaker', 'threads', 'codec_threads', 'seed', 'steps', 'top_k', 'chunk_frames',
        'codec_queue_depth', 'codec_history_frames', 'codec_future_frames', 'window_ms')] + [
        ('temperature', c.c_float), ('override_temperature', c.c_bool), ('cfg_scale', c.c_float),
        ('override_cfg_scale', c.c_bool), ('use_cfg', c.c_bool), ('use_local_transformer', c.c_bool),
        ('use_kv_cache', c.c_bool), ('use_stateful_codec', c.c_bool), ('codec_cpu', c.c_bool),
        ('flush_partial_chunk', c.c_bool), ('verbose', c.c_bool), ('lt_backend', c.c_int),
        ('sampling_backend', c.c_int), ('uma_mode', c.c_int), ('longform_mode', c.c_int), ('lt_fp32', c.c_bool)]


class Config(c.Structure):
    _fields_ = [('size', c.c_size_t), ('model', c.POINTER(Model)), ('runtime', c.POINTER(Runtime)),
                ('language', c.c_char_p), ('voice', c.c_char_p)]


class Options(c.Structure):
    _fields_ = [('size', c.c_size_t), ('request_id', c.c_char_p), ('language', c.c_char_p),
                ('speaker', c.c_int32), ('seed', c.c_int32), ('steps', c.c_int32), ('top_k', c.c_int32),
                ('temperature', c.c_float), ('override_temperature', c.c_bool),
                ('cfg_scale', c.c_float), ('override_cfg_scale', c.c_bool),
                ('voice', c.c_char_p), ('rate', c.c_int32)]


def synthesis_error(code, detail):
    """Explain known failures without copying note text from native diagnostics."""
    if 'unknown voice_name' in detail or 'speaker' in detail:
        return 'The selected voice is not supported by this model.'
    if 'language' in detail or 'tokenizer' in detail:
        return 'Speech text preparation failed. Check the language and tokenizer files.'
    if code == 2:
        return 'The speech runtime ran out of memory.'
    if code == 4:
        return 'Speech generation was cancelled by the runtime.'
    return f'Native speech generation failed (status {code}). Try a shorter selection or restart the runtime.'


def main():
    if sys.platform != 'win32':
        import resource
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    # Only the protocol carries note data. Discard native diagnostics at the source.
    output = os.fdopen(os.dup(sys.stdout.fileno()), 'w', buffering=1)
    with open(os.devnull, 'w') as diagnostics:
        os.dup2(diagnostics.fileno(), sys.stdout.fileno())
        os.dup2(diagnostics.fileno(), sys.stderr.fileno())

    def send(**event):
        output.write(json.dumps(event) + '\n')
        output.flush()

    handle = c.c_void_p()
    lib = None
    try:
        conf = json.loads(sys.stdin.readline())
        if sys.platform == 'win32':
            dll_directory = os.add_dll_directory(os.path.dirname(conf['library']))
        lib = c.CDLL(conf['library'])
        lib.nemo_speech_tts_version.restype = c.c_char_p
        if lib.nemo_speech_tts_version().decode() != 'nemo-speech-tts 0.1.0':
            raise RuntimeError('Native speech library must be version 0.1.0.')
        lib.nemo_speech_tts_last_error.restype = c.c_char_p
        lib.nemo_speech_tts_create.argtypes = [c.POINTER(Config), c.POINTER(c.c_void_p)]
        lib.nemo_speech_tts_destroy.argtypes = [c.c_void_p]
        lib.nemo_speech_tts_sample_rate.argtypes = [c.c_void_p]
        lib.nemo_speech_tts_synthesis_options_default.restype = Options
        lib.nemo_speech_tts_runtime_config_default.restype = Runtime
        callback_type = c.CFUNCTYPE(c.c_bool, c.POINTER(c.c_uint8), c.c_size_t, c.c_void_p)
        lib.nemo_speech_tts_synthesize_text.argtypes = [
            c.c_void_p, c.POINTER(Options), c.c_char_p, callback_type, c.c_void_p, c.c_void_p]
        model = Model(c.sizeof(Model), *(value.encode() for value in conf['paths']), None)
        runtime = lib.nemo_speech_tts_runtime_config_default()
        # 0.1.0 can fail when carrying history across short Markdown headings.
        # The controller already bounds requests; no long-form history is needed.
        runtime.longform_mode = 1  # NEMO_SPEECH_TTS_LONGFORM_OFF
        config = Config(c.sizeof(Config), c.pointer(model), c.pointer(runtime), b'en-US', None)
        if lib.nemo_speech_tts_create(c.byref(config), c.byref(handle)):
            raise RuntimeError('Native model initialization failed. Check the model files and runtime libraries.')
        send(ready=lib.nemo_speech_tts_sample_rate(handle))

        @callback_type
        def pcm(data, size, _):
            try:
                send(pcm=base64.b64encode(c.string_at(data, size)).decode('ascii'))
                # Backpressure: at most one native chunk awaits consumption by the audio sink.
                return sys.stdin.readline().strip() == 'continue'
            except (OSError, BrokenPipeError):
                return False

        for line in sys.stdin:
            request = json.loads(line)
            options = lib.nemo_speech_tts_synthesis_options_default()
            options.language = request['language'].encode()
            options.voice = request['voice'].encode()
            options.speaker = -1
            code = lib.nemo_speech_tts_synthesize_text(
                handle, c.byref(options), request['text'].encode(), pcm, None, None)
            if code:
                # Native errors can contain note text: keep it out of UI logs.
                detail = (lib.nemo_speech_tts_last_error() or b'').decode(errors='replace')
                raise RuntimeError(synthesis_error(code, detail))
            send(done=True)
            request.clear()
            line = ''
    except Exception as exc:
        send(error=str(exc))
    finally:
        if lib and handle:
            lib.nemo_speech_tts_destroy(handle)
        if sys.platform == 'win32' and 'dll_directory' in locals():
            dll_directory.close()


if __name__ == '__main__':
    main()
