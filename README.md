# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/nimonandang15/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/nimonandang15/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image that sums up the world's news of Thursday 26 November 2026 — a dense broadsheet, "The World in One Day": a masthead with story/region/field counts (50 stories · 10 regions · 21 fields), five stat tiles, three lead stories with drawn scenes, a 12-story grid, a world map of where it happened, an also-on list and a date-check footer.

## The day's news

Leads:

1. **Drone attack kills two Italians in Kuwait as Gulf comes under fire** — a drone hits a Kuwaiti military site, killing two Italian technicians; Iran denies any role. Tehran says two tankers hit mines near Khasab in the Strait of Hormuz; a Houthi projectile hits the Saudi Aramco refinery at Jazan, killing one worker.
2. **Russian missiles hit Kyiv shopping centre; seven wounded** — 113 drones launched overnight; Kyiv says 87 missiles and drones were downed. Trump urges Putin to pull back from widening the war.
3. **Israeli strikes kill nine in Gaza, a third night of attacks** — a Hamas-appointed deputy education minister is among the dead, despite a ceasefire now a year old.

Plus 12 more stories in the grid — Hernández de Cos picked to lead the ECB, the Bank of Korea raising rates to 3.25%, the Macy's Thanksgiving parade postponed by storm, Nvidia halting server shipments to Southeast Asia, North Korea expelling a Swiss diplomat, leaked data putting Russian war dead near 490,000, the EU budget summit clashing over Ukraine aid, rain hampering the rescue at a flooded Indonesian gold mine, DR Congo Ebola passing 12,000 cases, Duran Duran guitarist Andy Taylor dying at 65, five nations buying 430 CV90 combat vehicles, and Serbia setting its presidential election for 27 December — and six also-on items (Brazil calling the US tariff plan 'unacceptable', India's $1.62bn for Nepal, Myanmar rejecting parts of the ICJ Rohingya ruling, Guinea-Bissau delaying elections to 2028, Abrego Garcia landing in Spain, the world topping 2°C above pre-industrial for six days running).

Sources: Reuters, BBC, Al Jazeera, AP — 26 Nov 2026.

`main.ts` (Node 22, standard library only) copies `entry.png` byte for byte to `/output/entry.png`, refusing anything that is not a whole PNG within the gate limits (≤ 1 MiB, ≤ 1024×1024). Both runs write the same bytes. The poster is drawn by `render.py` (PIL + DejaVu only).

## Run it

```sh
python3 render.py            # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
