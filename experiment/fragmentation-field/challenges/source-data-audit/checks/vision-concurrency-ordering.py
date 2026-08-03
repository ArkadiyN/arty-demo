"""Concurrent vision extraction must reassemble pages by index, never by completion.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 7 (pipeline diagnosis), the concurrency change.

The serial loop this replaces got page order for free -- `results.extend(...)`
in loop order. Sending chunks concurrently removes that guarantee: a slow chunk
now finishes after chunks that were submitted later. If ordering were taken from
completion, a document's pages would silently transpose, which is precisely the
"every digit correct, wrong row" defect class this whole audit exists to catch,
reintroduced by the performance fix.

So the property under test is not speed, it is that out-of-order *completion*
still produces in-order *output*. The stub below inverts the relationship
deliberately -- the earliest chunk sleeps longest -- so completion order is the
exact reverse of input order and any completion-ordered reassembly fails loudly.

No API calls, no PDF: the real chunk function is stubbed out, because what is
being checked is the driver's bookkeeping, not the transcription.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-concurrency-ordering.py
"""

import importlib.util
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[5]
SRC = ROOT / "src/utils"


def load_processor():
    """Import pdf-processor.py by path -- the hyphen makes it non-importable."""
    sys.path.insert(0, str(SRC))
    spec = importlib.util.spec_from_file_location("pdf_processor", SRC / "pdf-processor.py")
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {SRC / 'pdf-processor.py'}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakePage:
    """Stands in for a fitz.Page: the driver only ever reads `.number`."""

    def __init__(self, number):
        self.number = number

    def get_pixmap(self, dpi=None):
        raise AssertionError("chunk-size 1 must not render for bounding")


def main():
    pp = load_processor()
    n_pages = 12
    pages = [FakePage(i) for i in range(n_pages)]

    # Earliest chunk sleeps longest -> completion order reverses input order.
    def stub(chunk, client, model, limiter=None):
        if limiter is not None:
            limiter.acquire()
        time.sleep(0.02 * (n_pages - chunk[0].number))
        return [(f"page-{p.number}", False) for p in chunk]

    pp._extract_doc_via_vision_google_chunk = stub

    started = time.monotonic()
    results = pp._extract_doc_via_vision_google(
        pages, client=None, model="stub", chunk_size=1, concurrency=8)
    wall = time.monotonic() - started

    got = [md for md, _ in results]
    want = [f"page-{i}" for i in range(n_pages)]
    ordered = got == want
    print(f"pages out: {got}")
    print(f"in input order: {ordered}")

    # Serial lower bound is the sum of the sleeps; 8-wide must beat it clearly.
    serial = sum(0.02 * (n_pages - i) for i in range(n_pages))
    print(f"\nwall {wall:.2f}s vs serial lower bound {serial:.2f}s "
          f"({serial / wall:.1f}x)")
    concurrent_enough = wall < serial / 2

    # The pacer is the quota guard: 30 starts must be admitted at once, the
    # 31st held. Checked directly rather than inferred from the run above,
    # which is deliberately too small to reach the limit.
    limiter = pp._RateLimiter(30)
    for _ in range(30):
        limiter.acquire()
    held_start = time.monotonic()
    limiter._starts[0] -= 59.5          # pretend the window opened 59.5 s ago
    limiter.acquire()
    held = time.monotonic() - held_start
    print(f"31st request held {held:.2f}s (expected ~0.55s)")
    paced = 0.3 < held < 1.5

    ok = ordered and concurrent_enough and paced
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'} — "
          f"ordering={ordered}, concurrent={concurrent_enough}, paced={paced}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
