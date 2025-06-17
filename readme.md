*************************************************************
Probity Data Filter Tool
*************************************************************



Common file types such as PNG, MP3, MP4, HTML, GZIP, JSON, CSV, TAR, WAV, EXE,
BAT and SH now
have dedicated engines. Engine detection runs all registered engines in parallel
for faster results. Use ``--only`` to limit scanning to particular engines.

Use the ``--only`` option to restrict detection to specific engines for faster
scans, for example:

```bash
python -m fastbackfilter.cli one sample.wav --only wav
```

You can also restrict directory scans to specific file extensions using
``--ext``:

```bash
python -m fastbackfilter.cli all mydir --ext exe sh
```

## Logging
=======

Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

*************************************************************
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
*************************************************************
A JSON schema describing the detection result format is provided in `fastbackfilter/detection_schema.json`.

