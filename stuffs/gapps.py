import os
import shutil
from stuffs.general import General
from tools.helper import get_download_dir, host, print_color, run, bcolors

class Gapps(General):
    dl_links = {
            "x86_64": ["https://nchc.dl.sourceforge.net/project/opengapps/x86_64/20220503/open_gapps-x86_64-10.0-pico-20220503.zip", "5fb186bfb7bed8925290f79247bec4cf"],
            "x86": ["https://cfhcable.dl.sourceforge.net/project/opengapps/x86/20220503/open_gapps-x86-10.0-pico-20220503.zip", "7fc75ec9bdca8def07bad306345ce877"],
            "arm64-v8a": ["https://nchc.dl.sourceforge.net/project/opengapps/arm64/20220503/open_gapps-arm64-10.0-pico-20220503.zip", "2feaf25d03530892c6146687ffa08bc2"],
            "armeabi-v7a": ["https://cfhcable.dl.sourceforge.net/project/opengapps/arm/20220215/open_gapps-arm-10.0-pico-20220215.zip", "1d00ffa4594734d477b10f2e0ee19c0b"]
        }
    arch = host()
    print("arch: "+str(arch))
    download_loc = get_download_dir()
    dl_link = dl_links[arch[0]][0]
    dl_file_name = os.path.join(download_loc, "open_gapps.zip")
    act_md5 = dl_links[arch[0]][1]
    copy_dir = "./gapps"
    extract_to = "/tmp/ogapps/extract"
    non_apks = [
        "vending-common.tar.lz",
        "defaultetc-common.tar.lz",
        "defaultframework-common.tar.lz",
        "googlepixelconfig-common.tar.lz"
        ]

    if arch == ('x86_64', 64):
        skip_1 = 'setupwizarddefault-x86_64.tar.lz'
        skip_2 = "setupwizardtablet-x86_64.tar.lz"
        
    if arch == ('arm64-v8a', 64):
        skip_1 = 'setupwizarddefault-arm64.tar.lz'
        skip_2 = "setupwizardtablet-arm64.tar.lz"
    skip = [
        skip_1,
        skip_2
        ]

    def download(self):
        print_color("Downloading OpenGapps now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.extract_to):
            os.makedirs(self.extract_to)
        if not os.path.exists(os.path.join(self.extract_to, "appunpack")):
            os.makedirs(os.path.join(self.extract_to, "appunpack"))

        for lz_file in os.listdir(os.path.join(self.extract_to, "Core")):
            for d in os.listdir(os.path.join(self.extract_to, "appunpack")):
                shutil.rmtree(os.path.join(self.extract_to, "appunpack", d))
            if lz_file not in self.skip:
                if lz_file not in self.non_apks:
                    print("    Processing app package : "+os.path.join(self.extract_to, "Core", lz_file))
                    run(["tar", "--lzip", "-xvf", os.path.join(self.extract_to, "Core", lz_file), "-C", os.path.join(self.extract_to, "appunpack")])
                    app_name = os.listdir(os.path.join(self.extract_to, "appunpack"))[0]
                    xx_dpi = os.listdir(os.path.join(self.extract_to, "appunpack", app_name))[0]
                    app_priv = os.listdir(os.path.join(self.extract_to, "appunpack", app_name, "nodpi"))[0]
                    app_src_dir = os.path.join(self.extract_to, "appunpack", app_name, xx_dpi, app_priv)
                    for app in os.listdir(app_src_dir):
                        shutil.copytree(os.path.join(app_src_dir, app), os.path.join(self.copy_dir, "system", "priv-app", app), dirs_exist_ok=True)
                else:
                    print("    Processing extra package : "+os.path.join(self.extract_to, "Core", lz_file))
                    run(["tar", "--lzip", "-xvf", os.path.join(self.extract_to, "Core", lz_file), "-C", os.path.join(self.extract_to, "appunpack")])
                    app_name = os.listdir(os.path.join(self.extract_to, "appunpack"))[0]
                    common_content_dirs = os.listdir(os.path.join(self.extract_to, "appunpack", app_name, "common"))
                    for ccdir in common_content_dirs:
                        shutil.copytree(os.path.join(self.extract_to, "appunpack", app_name, "common", ccdir), os.path.join(self.copy_dir, "system", ccdir), dirs_exist_ok=True)
