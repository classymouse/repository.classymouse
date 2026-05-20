import shutil, hashlib, re, os

repo_dir = r'C:\Users\fvanb\AppData\Roaming\Kodi\addons\repository.classymouse'
addon_src = r'C:\Users\fvanb\AppData\Roaming\Kodi\addons\plugin.video.classysbase'

# 1. copy new zip
src_zip = os.path.join(addon_src, r'tools\plugin.video.classysbase-1.0.5.zip')
dst_zip = os.path.join(repo_dir, r'plugin.video.classysbase\plugin.video.classysbase-1.0.5.zip')
shutil.copy2(src_zip, dst_zip)
print(f'Copied zip -> {dst_zip}')

# 2. copy addon.xml from the addon source
src_xml = os.path.join(addon_src, 'addon.xml')
dst_xml = os.path.join(repo_dir, r'plugin.video.classysbase\addon.xml')
shutil.copy2(src_xml, dst_xml)
print('Updated plugin.video.classysbase/addon.xml')

# 3. read it for embedding in addons.xml
with open(src_xml, 'r', encoding='utf-8') as f:
    inner = f.read()
# strip xml declaration
inner = re.sub(r'<\?xml[^?]*\?>\s*', '', inner).strip()

# 4. read existing addons.xml to preserve the repository.classymouse entry
addons_xml_path = os.path.join(repo_dir, 'addons.xml')
with open(addons_xml_path, 'r', encoding='utf-8') as f:
    existing = f.read()

# extract repository.classymouse addon block
repo_block = re.search(r'(<addon id="repository\.classymouse".*?</addon>)', existing, re.DOTALL)
repo_entry = repo_block.group(1) if repo_block else ''

new_addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n  ' + inner + '\n  ' + repo_entry + '\n</addons>\n'

with open(addons_xml_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_addons_xml)
print('Updated addons.xml')
print(new_addons_xml[:500])

# 5. regenerate md5
md5 = hashlib.md5(new_addons_xml.encode('utf-8')).hexdigest()
md5_path = os.path.join(repo_dir, 'addons.xml.md5')
with open(md5_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(md5)
print(f'Updated addons.xml.md5: {md5}')
