import argparse
import subprocess
import pathlib
import sys

from simple_erddap_metrics import parse_logs


def main():

    parser = argparse.ArgumentParser(
        description="Simple ERDDAP metrics dashboard and log exporter"
    )

    parser.add_argument(
        "-e", "--export",
        nargs="?",
        const="out.csv",
        help="Export parsed logs to CSV instead of launching the dashboard "
             "(default: out.csv)"
    )

    parser.add_argument(
        "-l", "--logs",
        help="Directory containing ERDDAP log files"
    )

    parser.add_argument(
        "-c", "--config",
        help="Optional YAML configuration file"
    )

    parser.add_argument(
        "--enable-geo",
        action="store_true",
        help="Enable IP geolocation lookup (slower parsing)"
    )

    args = parser.parse_args()

    # EXPORT MODE
    if args.export:

        if not args.logs:
            print("Error: -l/--logs is required when using -e/--export")
            sys.exit(1)

        out_path = pathlib.Path(args.export)

        print("Parsing logs...")

        df, _, _ = parse_logs(
            args.logs,
            geolocate=args.enable_geo,
            config_path=args.config
        )

        df.to_csv(out_path, index=False)

        print(f"CSV exported to: {out_path.resolve()}")

        return

    # STREAMLIT MODE
    app_path = pathlib.Path(__file__).parent / "streamlit_app.py"

    if not app_path.exists():
        print(f"Streamlit app not found: {app_path}")
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
    ]

    # argumentos para la app
    app_args = []

    if args.logs:
        app_args += ["--logs", args.logs]

    if args.config:
        app_args += ["--config", args.config]

    if args.enable_geo:
        app_args += ["--enable-geo"]

    if app_args:
        cmd += ["--"] + app_args

    subprocess.run(cmd, check=True)