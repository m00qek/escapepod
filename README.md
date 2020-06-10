# Old EscapePod feed

Creates a RSS feed containing episodes that are not in the main EscapePod feed
anymore.

The idea is to keep the same description, images, etc. as they were when the 
original feeds were available.

### How to use it?

Just point your podcast player to the link of `old-episodes.xml` in the 
[latest release](https://github.com/m00qek/escapepod/releases/latest).

### How does it work?

I got all feeds from snapshots of EscapePod website in the 
[Wayback Machine](https://web.archive.org/web/20200524210701/https://escapepod.org/)
and joined them using 

```bash
./split.py
./build.py
```

this command will generate the feed in `generated/feeds/old-episodes.xml`.
