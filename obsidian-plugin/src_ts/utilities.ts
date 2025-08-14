import { Notice, MarkdownView, TFile } from 'obsidian';
import * as path from 'path';
import MyPlugin from './main';

export default class UtilityManager {
    private plugin: MyPlugin;

    constructor(plugin: MyPlugin) {
        this.plugin = plugin;
    }
    
    getEditor(): any {
        const view = this.plugin.app.workspace.getActiveViewOfType(MarkdownView);
        return view?.editor;
    }
    
    async setStoryModelNumber(modelInt: string): Promise<void> {
        const activeFile = this.plugin.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('No active file');
            return;
        }

        const activeFileFolder = activeFile.parent;
        const settingsFilePath = activeFileFolder?.path + '/Settings/Settings.md';
        const settingsFile = this.plugin.app.vault.getAbstractFileByPath(settingsFilePath) as TFile;
        
        if (!settingsFile || settingsFile.extension !== 'md') {
            new Notice('Settings file not found at ./Settings/Settings.md');
            return;
        }

        await this.plugin.app.fileManager.processFrontMatter(settingsFile, (frontmatter: any) => {
            frontmatter.model = modelInt;
        });
    }

    async setChatModelNumber(modelInt: string): Promise<void> {
        const activeFile = this.plugin.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('No active file');
            return;
        }

        await this.plugin.app.fileManager.processFrontMatter(activeFile, (frontmatter: any) => {
            frontmatter.model = modelInt;
        });
    }

    async setModelNumber(modelInt: string): Promise<void> {
        const chatMode = await this.getMode();
        
        if (chatMode) {
            await this.setChatModelNumber(modelInt);
        } else {
            await this.setStoryModelNumber(modelInt);
        }
    }

    async getMode(): Promise<boolean> {
        const note = this.plugin.app.workspace.getActiveFile();
        if (!note) return false;
        
        const content = await this.plugin.app.vault.read(note);
        return /```\s*Custom instructions:/i.test(content);
    }

    getPartNumber(): number {
        const editor = this.getEditor();
        if (!editor) return 1;
        
        const cursor = editor.getCursor();

        // Get text from beginning of document to cursor position
        const textBeforeCursor = editor.getRange({line: 0, ch: 0}, cursor);

        // Count occurrences of the configured separator before cursor
        const escapedSeparator = this.plugin.settings.separator.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(escapedSeparator, 'g');
        const matches = textBeforeCursor.match(regex);
        let count = matches ? matches.length : 0;
        count = count + 1;

        return count;
    }

    getPaths(): [string, string] {
        const activeFile = this.plugin.app.workspace.getActiveFile();

        if (!activeFile) {
            console.log('No file is currently open');
            return ['', ''];
        }

        const vaultPath = (this.plugin.app.vault.adapter as any).basePath;
        const folderPath = activeFile.parent?.path || '';

        const absoluteFolderPath = path.join(vaultPath, folderPath);
        const absoluteFilePath = path.join(vaultPath, activeFile.path);

        return [absoluteFolderPath, absoluteFilePath];
    }
}
