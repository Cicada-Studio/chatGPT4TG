import os
import yaml
import dotenv
from pathlib import Path
from string import Template

config_dir = Path(__file__).parent.parent.resolve() / "config"

# Step 1: 讀取原始 config.yml（純文字）
with open(config_dir / "config.yml", 'r', encoding='utf-8') as f:
    raw_config = f.read()
# Step 2: 替換 ${...} 為對應的環境變數（os.environ）
template = Template(raw_config)
rendered_config = template.safe_substitute(os.environ)
# Step 3: 解析為 dict
config_yaml = yaml.safe_load(rendered_config)

# load .env config
config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
telegram_token = config_yaml["telegram_token"]
openai_api_key = config_yaml["openai_api_key"]
openai_api_base = config_yaml.get("openai_api_base", None)

#allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
raw_allowed = config_yaml.get("allowed_telegram_usernames", "")

if isinstance(raw_allowed, int):
    allowed_telegram_usernames = [raw_allowed]
elif isinstance(raw_allowed, str):
    allowed_telegram_usernames = [u.strip() for u in raw_allowed.split(",") if u.strip()]
elif isinstance(raw_allowed, list):
    allowed_telegram_usernames = raw_allowed
else:
    allowed_telegram_usernames = []
    
new_dialog_timeout = config_yaml["new_dialog_timeout"]
enable_message_streaming = config_yaml.get("enable_message_streaming", True)
return_n_generated_images = config_yaml.get("return_n_generated_images", 1)
image_size = config_yaml.get("image_size", "512x512")
n_chat_modes_per_page = config_yaml.get("n_chat_modes_per_page", 5)
mongodb_uri = f"mongodb://mongo:{config_env['MONGODB_PORT']}"

# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)

# models
with open(config_dir / "models.yml", 'r') as f:
    models = yaml.safe_load(f)

# files
help_group_chat_video_path = Path(__file__).parent.parent.resolve() / "static" / "help_group_chat.mp4"
