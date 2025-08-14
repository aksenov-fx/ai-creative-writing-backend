import { Plugin } from 'obsidian';
import { MyPluginSettings } from './types';
import { DEFAULT_SETTINGS } from './constants';
import CommandManager from './commands';
import CommunicationManager from './communication';
import UtilityManager from './utilities';
import HelperManager from './helpers';
import MyPluginSettingTab from './settings';

export default class MyPlugin extends Plugin {
    settings: MyPluginSettings;
    commandManager: CommandManager;
    communicationManager: CommunicationManager;
    utilityManager: UtilityManager;
    helperManager: HelperManager;

    async onload() {
        await this.loadSettings();
        
        // Initialize managers
        this.commandManager = new CommandManager(this);
        this.communicationManager = new CommunicationManager(this);
        this.utilityManager = new UtilityManager(this);
        this.helperManager = new HelperManager(this);
        
        // Add settings tab
        this.addSettingTab(new MyPluginSettingTab(this.app, this));

        // Register all commands
        this.commandManager.registerAllCommands();
    }
    
    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}
