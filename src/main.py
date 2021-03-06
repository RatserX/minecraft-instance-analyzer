#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import string
import typing
import requests
import validators

import analyzer
import helper
import logger

def main():
    base_path: str = os.path.dirname(__file__)
    
    analyzer_configuration_file: str = os.path.join(base_path, "../public/configuration/analyzer.json")
    file_public_path: str = os.path.join(base_path, "../public/file")
    log_public_path: str = os.path.join(base_path, "../public/log")
    profile_public_path: str = os.path.join(base_path, "../public/profile")

    logger_instance: logger.Logger = logger.Logger("logger")

    logger_instance.set_directory(log_public_path)
    logger_instance.set_level(logger.alog.INFO)
    
    with open(analyzer_configuration_file, "r") as fp:
        analyzer_option: dict = json.load(fp)
    
    profiles: list[dict] = analyzer_option["profiles"]
    profile_index: int = 0
    profile_length: int = len(profiles)

    if (profile_length > 0):
        while True:
            helper.Void.print_clear_all()
            logger_instance.info("Profiles:")
            
            for i in range(profile_length):
                profile: dict = profiles[i]
                name: str = profile["name"]
                
                logger_instance.info(f"[{i}] - {name}")
            
            input_index: int = helper.Number.input_numeric(f"Select profile (Default '{profile_index}'): ", profile_length, 0, profile_index)

            if (input_index >= 0):
                profile_index = input_index

                break
            
            logger_instance.warn("Invalid profile")

    profile: dict = profiles[profile_index]
    location_template: string.Template = string.Template(profile["location"])
    location: str = location_template.substitute({
        "PROFILE_PUBLIC_PATH": profile_public_path
    })
    
    analyzer_instance: dict = {}

    if (os.path.isfile(location)):
        location_file: str = os.path.join(profile_public_path, location)

        with open(location_file, "r") as fp:
            analyzer_instance = json.load(fp)
    elif (validators.url(location)):
        with requests.get(location) as response:
            analyzer_instance = response.json()
    
    def analyzer_progress_callback(analyzer_progress: analyzer.AnalyzerProgress) -> typing.Union[str, None]:
        analyzer_progress_message: typing.Union[list[str], None] = analyzer_progress.message
        analyzer_progress_state: str = analyzer_progress.state
        
        if (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_INFO_ADDON_INSTALL_DRAFT):
            installed_file_display_name: str = analyzer_progress_message[0]
            installed_file_download_url: str = analyzer_progress_message[1]
            installed_file_file_date: str = analyzer_progress_message[2]
            installed_file_file_name: str = analyzer_progress_message[3]
            
            logger_instance.info_append(f"Drafting addon installation . . .")
            logger_instance.info_append(f"Display name: {installed_file_display_name}")
            logger_instance.info_append(f"Download URL: {installed_file_download_url}")
            logger_instance.info_append(f"File date: {installed_file_file_date}")
            logger_instance.info_append(f"File name: {installed_file_file_name}")
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_INFO_ADDON_INSTALL_OPTION):
            installed_file_display_name: str = analyzer_progress_message[0]
            installed_file_download_url: str = analyzer_progress_message[1]
            installed_file_file_date: str = analyzer_progress_message[2]
            installed_file_file_name: str = analyzer_progress_message[3]

            addon_install_option: str = None

            while True:
                helper.Void.print_clear_all()

                input_addon_install_option: str = helper.String.input_option(f"Verifying addon '{installed_file_display_name}' (Y: Process installation; N: Skip installation; A: Install everything): ", ["A", "N", "Y"])

                if (input_addon_install_option is not None):
                    addon_install_option: str = input_addon_install_option.upper()

                    break
                
                logger_instance.warn("Invalid addon install option")
            
            logger_instance.info_append(f"--- ADDON ---")

            return addon_install_option
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_INFO_INSTANCE_INSTALL_PATH):
            install_path: str = analyzer_progress_message[0]
            name: str = analyzer_progress_message[1]

            if (install_path is None):
                install_path = os.path.normpath(file_public_path)
                instance_install_path: str = install_path
            else:
                instance_install_path: str = os.path.normpath(install_path)

            while True:
                helper.Void.print_clear_all()

                input_instance_install_path: str = helper.String.input_path(f"Select install path (Default '{install_path}'): ", instance_install_path)
                
                if (input_instance_install_path is not None):
                    instance_install_path = input_instance_install_path

                    break
                
                logger_instance.warn("Invalid instance install path")
            
            logger_instance.info_append(f"--- INSTANCE ---")
            logger_instance.info_append(f"Install path: {instance_install_path}")
            logger_instance.info_append(f"Name: {name}")
            
            return instance_install_path
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_INFO_LOADER_INSTALL_DRAFT):
            base_mod_loader_date_modified: str = analyzer_progress_message[0]
            base_mod_loader_download_url: str = analyzer_progress_message[1]
            base_mod_loader_file_name: str = analyzer_progress_message[2]
            base_mod_loader_forge_version: str = analyzer_progress_message[3]
            base_mod_loader_minecraft_version: str = analyzer_progress_message[4]
            base_mod_loader_name: str = analyzer_progress_message[5]
            
            logger_instance.info_append(f"Drafting loader installation . . .")
            logger_instance.info_append(f"Date Modified: {base_mod_loader_date_modified}")
            logger_instance.info_append(f"Download URL: {base_mod_loader_download_url}")
            logger_instance.info_append(f"File Name: {base_mod_loader_file_name}")
            logger_instance.info_append(f"Forge Version: {base_mod_loader_forge_version}")
            logger_instance.info_append(f"Minecraft Version: {base_mod_loader_minecraft_version}")
            logger_instance.info_append(f"Name: {base_mod_loader_name}")
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_INFO_LOADER_INSTALL_OPTION):
            base_mod_loader_date_modified: str = analyzer_progress_message[0]
            base_mod_loader_download_url: str = analyzer_progress_message[1]
            base_mod_loader_file_name: str = analyzer_progress_message[2]
            base_mod_loader_forge_version: str = analyzer_progress_message[3]
            base_mod_loader_minecraft_version: str = analyzer_progress_message[4]
            base_mod_loader_name: str = analyzer_progress_message[5]
            
            loader_install_option: str = None

            while True:
                helper.Void.print_clear_all()

                input_loader_install_option: str = helper.String.input_option(f"Verifying loader '{base_mod_loader_name}' (Y: Process installation; N: Skip installation; A: Install everything): ", ["A", "N", "Y"])

                if (input_loader_install_option is not None):
                    loader_install_option: str = input_loader_install_option.upper()

                    break
                
                logger_instance.warn("Invalid loader install option")
            
            logger_instance.info_append(f"--- LOADER ---")

            return loader_install_option
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_WARN_ADDON_INSTALL_SKIP):
            installed_file_display_name: str = analyzer_progress_message[0]
            installed_file_download_url: str = analyzer_progress_message[1]
            installed_file_file_date: str = analyzer_progress_message[2]
            installed_file_file_name: str = analyzer_progress_message[3]
            
            logger_instance.warn_append(f"Skipping addon installation . . .")
        elif (analyzer_progress_state == analyzer.AnalyzerState.ANALYZER_WARN_LOADER_INSTALL_SKIP):
            base_mod_loader_date_modified: str = analyzer_progress_message[0]
            base_mod_loader_download_url: str = analyzer_progress_message[1]
            base_mod_loader_file_name: str = analyzer_progress_message[2]
            base_mod_loader_forge_version: str = analyzer_progress_message[3]
            base_mod_loader_minecraft_version: str = analyzer_progress_message[4]
            base_mod_loader_name: str = analyzer_progress_message[5]
            
            logger_instance.warn_append(f"Skipping loader installation . . .")
        
        return None
    
    try:
        analyzer_instance = analyzer.Analyzer(analyzer_option, analyzer_instance)
        
        analyzer_instance.download(analyzer_progress_callback)
    except Exception as e:
        exception: analyzer.AnalyzerProgress = e.args[0]
        exception_message: typing.Union[list[str], None] = exception.message
        exception_state: str = exception.state

        if (exception_state == analyzer.AnalyzerState.ANALYZER_CRITICAL_ADDON_DOWNLOAD_PROGRESS):
            message: str = exception_message[0]
            installed_file_display_name: str = exception_message[1]
            installed_file_download_url: str = exception_message[2]
            installed_file_file_date: str = exception_message[3]
            installed_file_file_name: str = exception_message[4]
            
            logger_instance.critical_append(f"Cannot download file", f"Message: {message}", f"Display Name: {installed_file_display_name}", f"Download URL: {installed_file_download_url}", f"File Date: {installed_file_file_date}", f"File Name: {installed_file_file_name}")
        elif (exception_state == analyzer.AnalyzerState.ANALYZER_CRITICAL_LOADER_DOWNLOAD_PROGRESS):
            message: str = exception_message[0]
            base_mod_loader_date_modified: str = exception_message[1]
            base_mod_loader_download_url: str = exception_message[2]
            base_mod_loader_file_name: str = exception_message[3]
            base_mod_loader_forge_version: str = exception_message[4]
            base_mod_loader_minecraft_version: str = exception_message[5]
            base_mod_loader_name: str = exception_message[6]
            
            logger_instance.critical_append(f"Cannot download file", f"Message: {message}", f"Date Modified: {base_mod_loader_date_modified}", f"Download URL: {base_mod_loader_download_url}", f"File Name: {base_mod_loader_file_name}", f"Forge Version: {base_mod_loader_forge_version}", f"Minecraft Version: {base_mod_loader_minecraft_version}", f"Name: {base_mod_loader_name}")

main()
