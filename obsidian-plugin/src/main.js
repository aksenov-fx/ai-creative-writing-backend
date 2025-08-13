const { Plugin } = require('obsidian');
const { DEFAULT_SETTINGS } = require('./constants');
const CommandManager = require('./commands');
const CommunicationManager = require('./communication');
const UtilityManager = require('./utilities');
const MyPluginSettingTab = require('./settings');

class MyPlugin extends Plugin {
    async onload() {
        await this.loadSettings();
        
        // Initialize managers
        this.commandManager = new CommandManager(this);
        this.communicationManager = new CommunicationManager(this);
        this.utilityManager = new UtilityManager(this);
        
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

    // Delegate methods to utility manager
    async setModelNumber(modelInt) {
        return await this.utilityManager.setModelNumber(modelInt);
    }
    
    getPartNumber() {
        return this.utilityManager.getPartNumber();
    }

    getNotePath() {
        return this.utilityManager.getNotePath();
    }

    async rewriteSelection() {
        return await this.utilityManager.rewriteSelection();
    }
    
    async translateSelection() {
        return await this.utilityManager.translateSelection();
    }

    async explainWord() {
        return await this.utilityManager.explainWord();
    }

    // Delegate methods to communication manager
    async sendNoteCommand(methodName, selected_text = "") {
        return await this.communicationManager.sendNoteCommand(methodName, selected_text);
    }

    async sendCommandToServer(command) {
        return await this.communicationManager.sendCommandToServer(command);
    }
}

module.exports = MyPlugin;
