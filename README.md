
Setup Development Environment
------------------------------

1. Run in command window ```python makerelease.py```. This will create a zip file named ```plugin-video.desifreetv-x.x.x.zip```

2. In Kodi interface, select "Install addon from Zip File" and select the zip file created in previous step.

3. Once the plugin is installed successfully, shutdown Kodi.

4. ```Windows+R``` and type ```%appdata%\Kodi\addons```  in run dialog. Press Enter and windows explorer will open the folder.

5. Delete folder named ```plugin.video.desifreetv```.

6. Open a console window in the same directory and type ```mklink /D plugin.video.desifreetv <path/to/plugin.video.desifreetv/folder/in/git/repo/>```
 
