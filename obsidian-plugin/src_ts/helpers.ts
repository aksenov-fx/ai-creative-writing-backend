import { Notice } from 'obsidian';
import MyPlugin from './main';

export default class HelperManager {
    private plugin: MyPlugin;

    constructor(plugin: MyPlugin) {
        this.plugin = plugin;
    }

    private async _processSelection(command: string): Promise<string | null> {
        const editor = this.plugin.utilityManager.getEditor();
        if (!editor) {
            new Notice('No active editor');
            return null;
        }

        const selection = editor.getSelection();
        if (!selection) {
            new Notice('No selection found');
            return null;
        }

        const response = await this.plugin.communicationManager.sendNoteCommand(command, selection);
        
        if (!response) {
            new Notice('No response received');
            return null;
        }

        return response;
    }

    async rewriteSelection(): Promise<void> {
        const response = await this._processSelection('rewrite_selection');
        if (!response) return;

        const editor = this.plugin.utilityManager.getEditor();
        if (!editor) return;

        if (editor.somethingSelected()) {
            editor.replaceSelection(response);
        } else {
            new Notice('No selection found');
        }
    }

    async translateSelection(): Promise<void> {
        const response = await this._processSelection('translate');
        if (response) {
            new Notice(response);
        }
    }

    async explainWord(): Promise<void> {
        const response = await this._processSelection('explain');
        if (response) {
            new Notice(response);
        }
    }
}
