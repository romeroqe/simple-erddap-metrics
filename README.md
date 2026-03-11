# Simple ERDDAP Metrics

Simple ERDDAP Metrics is a lightweight tool to analyze ERDDAP server log files and visualize usage metrics through an interactive dashboard or export the parsed data as CSV.

## Features

- Parse ERDDAP log files automatically
- Detect dataset views and downloads
- Track file formats used
- Aggregate usage statistics (daily, monthly, yearly)
- Optional IP geolocation
- Interactive dashboard
- CSV export via CLI
- User-configurable formats and endpoints via YAML configuration

> [!IMPORTANT]
> This project is currently in **beta** and requires additional testing with large ERDDAP log archives.

## Installation

The package can be installed with:

```bash
pip install simple-erddap-metrics
```

## YAML Configuration File

Users can customize parsing behavior through a YAML configuration file.

### Fields
 
- `data_formats`: Defines which file extensions count as downloads (e.g., .csv, .nc). If a request uses one of these formats, it is classified as a download.
- `system_endpoints`: Defines ERDDAP internal endpoints that should be ignored (e.g., index, documentation). These are not counted as dataset interactions.

## Command Line Interface

The tool can be used either to launch the interactive dashboard or to export parsed logs to CSV.

### Interactive dashboard mode

Launch the dashboard:

```bash
simple-erddap-metrics
```

This will start the Streamlit interface.

### Export mode

Export parsed logs to CSV:

```bash
simple-erddap-metrics -e -l ./logs
```

This will generate the `out.csv` file.

### CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `-l`, `--logs` | in export mode | Directory containing ERDDAP log files |
| `-e`, `--export` | optional | Export parsed logs to CSV |
| `-c`, `--config` | optional | YAML configuration file |
| `--enable-geo` | optional | Enable IP geolocation |

#### Expected Log Files

The parser expects ERDDAP access logs such as:

```bash
log.txt
logArchivedAt...
logPreviousArchivedAt...
```

All files starting with `log` will be parsed.
