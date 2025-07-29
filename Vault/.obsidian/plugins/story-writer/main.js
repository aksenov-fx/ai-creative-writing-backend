const { Plugin, Notice, PluginSettingTab, Setting } = require('obsidian');
const net = require('net');
const path = require('path');

const DEFAULT_SETTINGS = {
    separator: '----'
};

class MyPlugin extends Plugin {
    async onload() {
        await this.loadSettings();
        
        this.addSettingTab(new MyPluginSettingTab(this.app, this));

        this.addCommand({
            id: 'set-prompt',
            hotkeys: [{ modifiers: ['Alt'], key: 'S' }],
            name: 'Set user prompt',
            callback: () => {
                new Notice(`Set user prompt`);
                this.sendNoteCommand('set_prompt');
            }
        });

        this.addCommand({
            id: 'write-scene',
            name: 'Write Scene',
            hotkeys: [{ modifiers: ['Alt'], key: 'W' }],
            callback: () => {
                new Notice(`Write Scene`);
                this.sendNoteCommand('write_scene');
            }
        });

        this.addCommand({
            id: 'custom-prompt',
            name: 'Custom Prompt',
            hotkeys: [{ modifiers: ['Alt'], key: 'C' }],
            callback: () => {
                new Notice(`Custom Prompt`);
                this.sendNoteCommand('custom_prompt');
            }
        });

        this.addCommand({
            id: 'remove-last-response',
            name: 'Remove Last Response',
            hotkeys: [{ modifiers: ['Alt'], key: 'Z' }],
            callback: () => {
                new Notice(`Remove Last Response`);
                this.sendNoteCommand('remove_last_response');
            }
        });

        this.addCommand({
            id: 'interrupt-write',
            name: 'Interrupt Write',
            hotkeys: [{ modifiers: ['Alt'], key: 'Q' }],
            callback: () => {
                new Notice(`Interrupt Write`);
                this.sendNoteCommand('interrupt_write');
            }
        });

        this.addCommand({
            id: 'rewrite',
            name: 'Rewrite',
            callback: () => {
                new Notice(`Rewrite`);
                this.sendNoteCommand('rewrite');
            }
        });

        this.addCommand({
            id: 'rewrite-parts',
            name: 'Rewrite this and following parts',
            callback: () => {
                new Notice(`Rewrite this and following parts`);
                this.sendNoteCommand('rewrite_parts');
            }
        });

        this.addCommand({
            id: 'regenerate',
            name: 'Regenerate',
            callback: () => {
                new Notice(`Regenerate`);
                this.sendNoteCommand('regenerate');
            }
        });

        this.addCommand({
            id: 'add-part',
            name: 'Add Part',
            callback: () => {
                new Notice(`Add Part`);
                this.sendNoteCommand('add_part');
            }
        });

        this.addCommand({
            id: 'summarize',
            name: 'Summarize story',
            callback: () => {
                new Notice(`Summarize story`);
                this.sendNoteCommand('summarize');
            }
        });

        this.addCommand({
            id: 'update-summary',
            name: 'Update summary',
            callback: () => {
                new Notice(`Update summary`);
                this.sendNoteCommand('update_summary');
            }
        });

        this.addCommand({
            id: 'set-model-1',
            name: 'Set model 1',
            hotkeys: [{ modifiers: ['Alt'], key: '1' }],
            callback: () => {
                new Notice(`Set model 1`);
                this.sendNoteCommand('set_model', 1);
            }
        });

        this.addCommand({
            id: 'set-model-2',
            name: 'Set model 2',
            hotkeys: [{ modifiers: ['Alt'], key: '2' }],
            callback: () => {
                new Notice(`Set model 2`);
                this.sendNoteCommand('set_model', 2);
            }
        });

        this.addCommand({
            id: 'set-model-3',
            name: 'Set model 3',
            hotkeys: [{ modifiers: ['Alt'], key: '3' }],
            callback: () => {
                new Notice(`Set model 3`);
                this.sendNoteCommand('set_model', 3);
            }
        });

        this.addCommand({
            id: 'enable-debug',
            name: 'Enable Debug Mode',
            callback: () => {
                new Notice(`Enable Debug Mode`);
                this.sendNoteCommand('enable_debug');
            }
        });

        this.addCommand({
            id: 'disable-debug',
            name: 'Disable Debug Mode',
            callback: () => {
                new Notice(`Enable Debug Mode`);
                this.sendNoteCommand('disable_debug');
            }
        });
    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }

    getPartNumber() {
        const editor = this.app.workspace.activeLeaf.view.editor
        const cursor = editor.getCursor()

        // Get text from beginning of document to cursor position
        const textBeforeCursor = editor.getRange({line: 0, ch: 0}, cursor)

        // Count occurrences of the configured separator before cursor
        const regex = new RegExp(this.settings.separator.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
        const matches = textBeforeCursor.match(regex)
        var count = matches ? matches.length : 0
        count = count + 1

        return count
    }

    getNotePath() {
        const activeFile = this.app.workspace.getActiveFile();
        if (activeFile) {
            const vaultPath = this.app.vault.adapter.basePath;
            const folderPath = activeFile.parent?.path || '';
            const absoluteFolderPath = path.join(vaultPath, folderPath);
            return absoluteFolderPath;
        } else {
            console.log('No file is currently open');
        }
    }

    sendNoteCommand(methodName, model_number = 0) {
        this.app.commands.executeCommandById('editor:save-file');

        var absoluteFolderPath = this.getNotePath();
        var partNumber = this.getPartNumber();
        var parameters = `${absoluteFolderPath},${methodName},${partNumber},${model_number}`;

        this.sendCommandToServer(parameters);
    }

    sendCommandToServer(command) {
        const client = new net.Socket();
        client.connect(9993, 'localhost', () => {
            console.log('Connected to Python server');
            client.write(command);
            client.destroy();
        });

        client.on('data', (data) => {
            console.log('Received: ' + data);
            client.destroy();
        });

        client.on('close', () => {
            console.log('Connection closed');
        });

        client.on('error', (err) => {
            console.error('Connection error: ', err);
        });
    }
}

class MyPluginSettingTab extends PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display() {
        const { containerEl } = this;

        containerEl.empty();

        containerEl.createEl('h2', { text: 'Plugin Settings' });

        new Setting(containerEl)
            .setName('Separator text')
            .setDesc('Text pattern to match for counting parts')
            .addText(text => text
                .setPlaceholder('----')
                .setValue(this.plugin.settings.separator)
                .onChange(async (value) => {
                    this.plugin.settings.separator = value;
                    await this.plugin.saveSettings();
                }));
    }
}

module.exports = MyPlugin;