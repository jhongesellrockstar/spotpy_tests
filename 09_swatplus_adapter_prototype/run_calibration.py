from config import load_config
cfg=load_config()
if str(cfg["SWAT_EXECUTABLE"]).startswith("REPLACE_"):
    print("SWATPLUS_PROTOTYPE_CONFIG_OK: no real SWAT+ execution attempted")
else:
    raise SystemExit("A path is configured, but deliberate activation requires adapting this script after project verification.")
