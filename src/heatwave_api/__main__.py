from typing import Optional, Sequence

from heatwave_api.rest_api import app


def main(*argv: Sequence[str]) -> Optional[int]:
    import uvicorn

    return uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    import sys

    sys.exit(main(*sys.argv))
