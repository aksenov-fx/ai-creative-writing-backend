const { Notice } = require('obsidian');
const path = require('path');

class UtilityManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    async setStoryModelNumber(modelInt) {
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
    
    }
    
    async setChatModelNumber(modelInt) {
        const activeFile = this.plugin.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('No active file');
            return;
        }

        await this.plugin.app.fileManager.processFrontMatter(activeFile, (frontmatter) => {
            frontmatter.model = modelInt;
        });

    }
    
    async setModelNumber(modelInt) {

        var chatMode = await this.getMode()

        if (chatMode) {
            await this.setChatModelNumber(modelInt)
        } else {
            await this.setStoryModelNumber(modelInt)
        }
    }
    
    async getMode() {
        const note = app.workspace.getActiveFile()
        const content = await app.vault.read(note)
        return /```\s*Custom instructions:/i.test(content)
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

    getPaths() {
        const activeFile = this.plugin.app.workspace.getActiveFile();

        if (!activeFile) {
            console.log('No file is currently open');
            return;
        }

        const vaultPath = this.plugin.app.vault.adapter.basePath;
        const folderPath = activeFile.parent?.path || '';

        const absoluteFolderPath = path.join(vaultPath, folderPath);
        const absoluteFilePath = path.join(vaultPath, activeFile.path);

        return [absoluteFolderPath, absoluteFilePath];
            
    }


}

module.exports = UtilityManager;