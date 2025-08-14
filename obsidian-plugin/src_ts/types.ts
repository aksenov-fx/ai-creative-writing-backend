import { Plugin, App, TFile, PluginSettingTab, Setting, Notice } from 'obsidian';

export interface MyPluginSettings {
    separator: string;
}

export interface CommandConfig {
    name: string;
    hotkeys?: Array<{
        modifiers: string[];
        key: string;
    }>;
    callback: () => void | Promise<void | string>;
}

export interface CommandsHash {
    [key: string]: CommandConfig;
}

export interface Paths {
    absoluteFolderPath: string;
    absoluteFilePath: string;
}
