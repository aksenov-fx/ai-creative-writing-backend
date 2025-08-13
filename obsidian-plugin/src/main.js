const { Plugin } = require('obsidian');
const { DEFAULT_SETTINGS } = require('./constants');
const CommandManager = require('./commands');
const CommunicationManager = require('./communication');
const UtilityManager = require('./utilities');
const HelperManager = require('./helpers');
const MyPluginSettingTab = require('./settings');

class MyPlugin extends Plugin {
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

module.exports = MyPlugin;