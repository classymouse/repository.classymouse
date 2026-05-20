import shutil, hashlib, re, os

repo_dir  = r'C:\Users\fvanb\AppData\Roaming\Kodi\addons\repository.classymouse'
addon_src = r'C:\Users\fvanb\AppData\Roaming\Kodi\addons\plugin.video.chainsnew'
zip_src   = r'C:\Users\fvanb\AppData\Roaming\Kodi\addons\plugin.video.classysbase\tools\chains_fork\plugin.video.chainsnew-1.0.4.zip'

addon_id  = 'plugin.video.chainsnew'
version   = '1.0.4'

# 1. create target dir
target_dir = os.path.join(repo_dir, addon_id)
os.makedirs(target_dir, exist_ok=True)

# 2. copy zip
shutil.copy2(zip_src, os.path.join(target_dir, f'{addon_id}-{version}.zip'))
print(f'Copied zip')

# 3. copy addon.xml, icon, fanart
for f in ('addon.xml', 'icon.png', 'fanart.jpg'):
    src = os.path.join(addon_src, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(target_dir, f))
        print(f'Copied {f}')

# 4. read addon.xml for addons.xml
with open(os.path.join(addon_src, 'addon.xml'), 'r', encoding='utf-8') as f:
    inner = f.read()
inner = re.sub(r'<\?xml[^?]*\?>\s*', '', inner).strip()

# 5. read current addons.xml, insert new addon, keep existing entries
addons_xml_path = os.path.join(repo_dir, 'addons.xml')
with open(addons_xml_path, 'r', encoding='utf-8') as f:
    existing = f.read()

# extract both existing addon blocks
classysbase_block = re.search(r'(<addon id="plugin\.video\.classysbase".*?</addon>)', existing, re.DOTALL)
repo_block        = re.search(r'(<addon id="repository\.classymouse".*?</addon>)', existing, re.DOTALL)

classysbase_entry = classysbase_block.group(1) if classysbase_block else ''
repo_entry        = repo_block.group(1) if repo_block else ''

new_addons_xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n  '
    + classysbase_entry + '\n  '
    + inner + '\n  '
    + repo_entry + '\n</addons>\n'
)

with open(addons_xml_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_addons_xml)
print('Updated addons.xml')

# 6. regenerate md5
md5 = hashlib.md5(new_addons_xml.encode('utf-8')).hexdigest()
with open(os.path.join(repo_dir, 'addons.xml.md5'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(md5)
print(f'Updated addons.xml.md5: {md5}')
