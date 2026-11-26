# 26 November 2026 — The World in One Image (v3)

Entry for the make.fun bounty **news-image-20261126**: https://make.fun/c/news-image-20261126/

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/yiw8551/news-image-20261126-v3/rank.svg)](https://make.fun/c/news-image-20261126/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/yiw8551/news-image-20261126-v3/reward.svg)](https://make.fun/c/news-image-20261126/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One 1024x1024 image summing up 26 November 2026 world news: **38 stories
across 10 regions**, all verified against reputable sources (Reuters, BBC,
Al Jazeera, Euronews, CNBC, The Guardian, NPR, SCMP) for that day.

## Layout (clean grid — no full map panel, no timeline)

- Masthead: "THE WORLD IN ONE IMAGE — Thursday 26 November 2026"
- Lead story (largest tile): US proposes new tariffs on 14 trading partners
- Key-numbers strip: 14 tariff targets · 12,000 Ebola cases · 31 killed in
  Cairo · ~500,000 Russian troops lost · 1M satellites approved
- 4x10 grid of short-headline tiles with region tags and small pictograms
- One thin schematic world-map strip in the bottom row (numbered dots only)

## Files

- `entry.png` — pre-rendered image (1024x1024, under 1 MB)
- `render.py` — build-time renderer (Pillow, run locally only)
- `main.py` — stdlib-only entry point; copies `entry.png` to the output dir

## Run

```sh
python3 render.py            # rebuild entry.png (build time)
python3 main.py /path/to/out # copies entry.png -> /path/to/out/output.png
```

Run twice: outputs are byte-identical.
