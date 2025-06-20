# config.py
import yaml
import torch
import os
_config = None  # internal singleton instance

class Config:
    def __init__(self, data):
        self.raw = data
        self.use_gpu = self._resolve_gpu(data.get('use_gpu', 'auto'))
        self.batch_size = data.get('batch_size', 8)
        self.threshold = data.get('threshold', 0.1)
        self.dataset_name = data.get('dataset_name')         # Change this to switch datasets
        self.data_is_video = data.get('data_is_video', 'false')
        self.base_data_dir = data.get('base_data_dir', 'data')
        self.base_results_dir = data.get('base_results_dir' , 'results')
        self.use_nerf = data.get('run_nerf', 'true')
        self.data_is_video = data.get('data_is_video', 'false')
        self.data_dir = os.path.join(self.base_data_dir, self.dataset_name)
        self.results_dir = os.path.join(self.base_results_dir, self.dataset_name)
        self.image_dir = os.path.join(self.data_dir, "images")
        self.video_dir = os.path.join(self.data_dir,  "video")
        self.mesh_dir = os.path.join(self.results_dir, "meshes")
        
    def _resolve_gpu(self, val): #resolve the gpu computation based on availability 
        if isinstance(val, str):
            val = val.lower()
        if val == 'auto' or val == 'true':
            try:
                return torch.cuda.is_available()
            except ImportError:
                return False
        return bool(val)
    
    def apply_overrides(self, args: dict):
        for key, val in args.items():
            if val is not None:
                setattr(self, key, val)
                self.raw[key] = val  # track effective config

def load_config(config_path="configs", config_name="config.yaml"): #function to load global config
    global _config
    config_file = os.path.join(config_path, config_name)
    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)
    _config = Config(data)

    
def get_config(): #function to get global config
    if _config is None:
        raise RuntimeError("Config not loaded. Call `load_config(path)` first.")
    return _config
