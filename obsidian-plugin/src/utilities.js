const { Notice } = require('obsidian');
const path = require('path');

class UtilityManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    async setModelNumber(modelInt) {
        const activeFile = this.plugin.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('No active file');
            return;
        }
    
        const activeFileFolder = activeFile.parent;
        const settingsFilePath = activeFileFolder.path + '/Settings/Settings.md';
        const settingsFile = this.plugin.app.vault.getAbstractFileByPath(settingsFilePath);
        
        if (!settingsFile || settingsFile.extension !== 'md') {
            new Notice('Settings file not found at ./Settings/Settings.md');
            return;
        }
    
        await this.plugin.app.fileManager.processFrontMatter(settingsFile, (frontmatter) => {
            frontmatter.model = modelInt;
        });
    
        // new Notice(`Model number updated to: ${modelInt}`);
    }
    
    getPartNumber() {
        const editor = this.plugin.app.workspace.activeLeaf.view.editor
        const cursor = editor.getCursor()

        // Get text from beginning of document to cursor position
        const textBeforeCursor = editor.getRange({line: 0, ch: 0}, cursor)

        // Count occurrences of the configured separator before cursor
        const regex = new RegExp(this.plugin.settings.separator.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
        const matches = textBeforeCursor.match(regex)
        var count = matches ? matches.length : 0
        count = count + 1

        return count
    }

    getNotePath() {
        const activeFile = this.plugin.app.workspace.getActiveFile();
        if (activeFile) {
            const vaultPath = this.plugin.app.vault.adapter.basePath;
            const folderPath = activeFile.parent?.path || '';
            const absoluteFolderPath = path.join(vaultPath, folderPath);
            return absoluteFolderPath;
        } else {
            console.log('No file is currently open');
        }
    }

    async rewriteSelection() {
        const editor = this.plugin.app.workspace.activeLeaf.view.editor;
        const selection = editor.getSelection();

        if (!selection) {
            new Notice('No selection found');
            return;
        }

        const response = await this.plugin.communicationManager.sendNoteCommand('rewrite_selection', selection);
        
        if (!response) { 
            new Notice('No response received');
            return;
        }

        if (editor.somethingSelected()) {
            editor.replaceSelection(response);
        }

        else {
            new Notice('No selection found');
        }
    }

    async translateSelection() {
        const editor = this.plugin.app.workspace.activeLeaf.view.editor;
        const selection = editor.getSelection();

        if (!selection) {
            new Notice('No selection found');
            return;
        }

        const response = await this.plugin.communicationManager.sendNoteCommand('translate', selection);
        
        if (!response) { 
            new Notice('No response received');
            return;
        }

        new Notice(response);

    }

}

module.exports = UtilityManager;
