# Importações de bibliotecas
import json
import os

def init_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "config.local.json")
    
    if not os.path.exists(config_path):
        config_path = "config/config.local.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    if config.get("env") == "dev":
        config["database"] = "CRS_HOMDB"
    else:
        config["database"] = "CRS"
        
    return config