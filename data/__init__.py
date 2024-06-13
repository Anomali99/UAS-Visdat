import os
_current_file_path = os.path.abspath(__file__)
root_dir = os.path.dirname(_current_file_path)

gempa_dirasakan = os.path.join(root_dir, "data-gempa-terbaru.json")
gempa_m5 = os.path.join(root_dir, "data-gempa-M5.0+.json")