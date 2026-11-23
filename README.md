# world-news-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/bioganteng75/world-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/bioganteng75/world-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A Node program that delivers one front-page image summing up the world news of Monday 23 November 2026: the COP31 collapse in Antalya, the Russian strike on Dymer, the AI stock sell-off and the Democrats' US House win, plus six more of the day's stories. The image is composed by `compose.py` from four illustrated panels in `assets/`; `main.ts` copies the finished `entry.png` to the output directory byte for byte.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes `out/entry.png`. To rebuild the image itself first, run `python3 compose.py` (needs Python 3 with Pillow), then run the command above.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rd8zvqpf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
