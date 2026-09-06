<!-- {"notolog.app": {"created": "2026-09-05 00:00:00.000000", "updated": "2026-09-06 00:00:00.000000"}} -->
# Text-to-Speech

Notolog's built-in Text-to-Speech module reads Markdown and plain-text documents aloud on your computer.
Read a whole document, selected text, or start from the cursor. Playback controls let you pause, resume,
and stop reading while you work.

## Set up local speech

For a pip installation, install the audio dependencies in the same Python environment as Notolog:

```sh
pip install "notolog[tts]"
```

This adds sounddevice for PCM audio playback through PortAudio. The base `pip install notolog` installation
includes the module's code but does not install these audio dependencies. On Linux, install
the PortAudio system library (on Debian/Ubuntu: `sudo apt install libportaudio2`). Windows
and macOS pip wheels include PortAudio. The Notolog Debian package declares this dependency automatically.

Model downloads also require `curl` and CA certificates. On Debian/Ubuntu, install the TTS prerequisites with
`sudo apt install libportaudio2 curl ca-certificates`. These are additional to the desktop libraries required by Qt.
If audio dependencies are missing, settings keep model setup available and show the required installation command
beside the disabled voice test. Restart Notolog after installing the dependencies.

1. Open **Settings → Text-to-Speech** and turn on **Enable Text-to-Speech** if it is off.
2. Use **Get runtime** to open the compatible NeMo-Speech.cpp release. Choose an archive for your operating
   system and processor architecture, then extract the entire archive. Keep its companion libraries and
   license files alongside the executable.
3. Under **Speech runtime**, select `bin/nemo-speech`, or `bin/nemo-speech.exe` on Windows.
4. Choose a writable **Model folder** and select **Download models**. Downloads need `curl`, internet access,
   and approximately 550 MB for the model set, in addition to the runtime.
5. Choose the document's **Language** and a **Voice**, then select **Test voice**.

The runtime and models are separate downloads. Use the release linked from your installed application's
settings: a newer upstream runtime is not necessarily compatible with its native interface.

**Details** shows download and verification output. Existing files are reused after verification;
**Verify models** also downloads missing or damaged files. Closing settings during a download asks whether
to cancel it. Completed downloads are retained for a later attempt.

## Read documents and selections

- Use **Read document aloud** or the editor's play control to read the current document.
- Select text in edit or view mode, then choose **Read selection aloud** from its context menu.
- Choose **Read from cursor aloud** from the edit or view context menu to start at that position.
- Use the file tree's read action to read a file. Open and unlock an encrypted note before reading it.
- Pause or resume with the pause control, and end playback with stop.

Hover over the soundwave icon beside the playback controls to inspect speech details such as voice,
language, audio format, runtime, and model paths.

## Voices, languages, and reading settings

The supplied model offers **John, Sofia, Aria, Jason, and Leo**. Aria is the default for a new setup.
These are voices within one speech model, rather than separate model downloads.

Choose the document language explicitly; Notolog does not detect it automatically or infer it from the
interface language. English is the default. Spanish, German, French, Italian, Vietnamese, and Hindi are
also available. Mandarin and Japanese require a runtime built with their respective language support.
The application's 19 interface translations do not imply 19 supported speech languages.
Changing the app's interface language immediately updates the speech settings and playback controls.
Application messages already shown in **Details** update too; native runtime output remains verbatim.
Your selected speech language stays the same, and active downloads or playback continue.

| Setting | Effect |
|---------|--------|
| **Context length** | Maximum characters per speech request. The far-right **Whole document** position preserves heading breaks; runtime limits still apply. |
| **Speed** | Adjusts playback speed, which also changes voice pitch. |
| **Announce headings** | Announces Markdown and HTML heading levels: Chapter, Section, Subsection, Sub-subsection, then Heading level 5 or 6. |
| **Skip inline code** | When checked, says “Inline code block”; when unchecked, reads the code contents. |
| **Skip multiline code** | When checked, says “Multiline code block”; when unchecked, reads fenced and indented code contents. |

Heading announcements and code labels use English. Reading source code aloud may pronounce punctuation
or identifiers differently from how a programmer would say them.

## Runtime and supported models

Notolog uses the native [NVIDIA NeMo-Speech.cpp](https://github.com/NVIDIA/NeMo-Speech.cpp) runtime through
a persistent local worker. It does not require installing the full Python NeMo toolkit or PyTorch for
speech playback. The default model set contains:

| Component | Model or assets |
|-----------|-----------------|
| Speech generator | [NVIDIA MagpieTTS Multilingual 357M v2602](https://huggingface.co/nvidia/magpie_tts_multilingual_357m/tree/v2602), in F16 GGUF format |
| Audio decoder | [NVIDIA NeMo NanoCodec 22 kHz](https://huggingface.co/nvidia/nemo-nano-codec-22khz-1.89kbps-21.5fps), in decoder F16 GGUF format |
| Tokenizers | Matching tokenizer and pronunciation assets from the Magpie model archive |

**Custom model files** can override the downloaded paths. They must form a compatible MagpieTTS,
NanoCodec, and tokenizer set; an arbitrary GGUF or NeMo model cannot be substituted. Clear the override
fields to return to the managed model folder.

## Performance and privacy

The worker keeps loaded models ready for subsequent speech requests and streams generated PCM audio
to PortAudio in memory. The first request includes model loading. Smaller contexts can reduce the
wait before playback; larger contexts provide more surrounding text but need more time and memory.
Generation speed depends on the selected runtime and hardware, so uninterrupted real-time playback
is not guaranteed. Streaming audio does not mean synthesizing each word independently.

After setup, speech generation runs locally without a cloud speech API. Model downloads contact Hugging
Face. Document text and generated audio pass through local pipes and memory without temporary text or
audio files. Model files remain on disk. Operating-system swap, crash dumps, and external recording are
outside this protection.

## Troubleshooting

| Symptom | What to check |
|---------|---------------|
| Speech controls are unavailable | Install the audio dependencies in the environment running Notolog, restart the application, and enable the module. |
| Runtime cannot load | Use the compatible release offered in Settings and extract the complete archive, including its companion libraries. Check the operating system and processor architecture. |
| macOS blocks `nemo-speech` or repeatedly asks to approve its libraries | Follow [macOS runtime approval](#macos-runtime-approval) before retrying the download or voice test. |
| Models are missing after changing folders | Download into the new folder, or select existing compatible files under **Custom model files**. |
| Windows downloads models but cannot load them | With runtime 0.1.0, non-ASCII model paths can fail. Choose a writable **Model folder** whose entire path uses ASCII characters, such as `C:\NotologModels`, and download there. Apply the same rule to custom model and tokenizer paths. |
| Download or verification fails | Expand **Details**. Check internet access, `curl`, free space, and write permission for the model folder. |
| Speech starts slowly or has gaps | Try a smaller context and close other heavy workloads. Initial model loading and generation both contribute to latency. |
| Pronunciation is wrong | Select the document's language explicitly and check whether the runtime supports it. |

### macOS runtime approval

On macOS, model downloads also run `nemo-speech`, so extracting the runtime is not enough if macOS blocks it.
If the alert says Apple could not verify the runtime and you trust the archive obtained through **Get runtime**,
click **Done**, open **System Settings → Privacy & Security**, select **Open Anyway** for `nemo-speech`,
and confirm. Then retry **Download models** or **Test voice**. See
[Apple's instructions for opening apps safely](https://support.apple.com/102445).

If macOS asks to approve each `libnemo_*` or other bundled library separately, these are runtime components,
not downloaded models. For a trusted archive whose SHA-256 matches the checksum published on the
[compatible release page](https://github.com/NVIDIA/NeMo-Speech.cpp/releases/tag/v0.1.0), you can remove
quarantine from the complete extracted runtime folder once. Replace the example path below with the folder
containing `bin` and `lib`, then run in Terminal:

```sh
xattr -dr com.apple.quarantine "/path/to/extracted/nemo-speech"
"/path/to/extracted/nemo-speech/bin/nemo-speech" --version
```

This bypasses quarantine prompts for that runtime and its bundled libraries; it does not verify their safety.
Keep the command scoped to the extracted runtime folder. It normally needs no `sudo` for files you own and
leaves system-wide Gatekeeper settings enabled. After the version check succeeds, retry **Download models**
or **Test voice**. A newly downloaded runtime may require this step again.

## Licenses

Notolog is MIT-licensed. Runtime, model, and audio-library licenses are separate; see the
[Text-to-Speech third-party notices](https://github.com/notolog/notolog-editor/blob/main/ThirdPartyNotices.md#text-to-speech).
The separately installed runtime includes its license and third-party notices under
`share/licenses/nemo-speech/`. Redistribution is governed by the licenses supplied with that runtime.
Notolog is not affiliated with or endorsed by NVIDIA.
