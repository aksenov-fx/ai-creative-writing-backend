const { Notice } = require('obsidian');

class HelperManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    _getEditor() {
        return this.plugin.app.workspace.activeLeaf.view.editor;
    }
    
    async _processSelection(command) {
        const editor = this._getEditor();
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

    async rewriteSelection() {
        const response = await this._processSelection('rewrite_selection');
        if (!response) return;

        const editor = this._getEditor();
        if (editor.somethingSelected()) {
            editor.replaceSelection(response);
        } else {
            new Notice('No selection found');
        }
    }

    async translateSelection() {
        const response = await this._processSelection('translate');
        if (response) {
            new Notice(response);
        }
    }

    async explainWord() {
        const response = await this._processSelection('explain');
        if (response) {
            new Notice(response);
        }
    }

}

module.exports = HelperManager;