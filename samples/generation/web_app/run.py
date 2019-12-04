#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

from .app import create_app

__author__ = "Christian Heider Nielsen"
__doc__ = ""

if __name__ == "__main__":
    executable_path = Path.home() / "Data"
    executable_path.mkdir(parents=True)
    exported_model_path = executable_path / "export"
    labels_path = executable_path / "output_labels.txt"
    app = create_app(exported_model_path, labels_path)
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
