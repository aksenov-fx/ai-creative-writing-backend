const { Notice } = require('obsidian');

class CommandManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    registerAllCommands() {
        this.registerWritingCommands();
        this.registerModelCommands();
        this.registerUtilityCommands();
    }

    registerWritingCommands() {
        this.plugin.addCommand({
            id: 'set-prompt',
            hotkeys: [{ modifiers: ['Alt'], key: 'S' }],
            name: 'Set user prompt',
            callback: () => {
                new Notice(`Set user prompt`);
                this.plugin.sendNoteCommand('set_prompt');
            }
        });

        this.plugin.addCommand({
            id: 'write-scene',
            name: 'Write Scene',
            hotkeys: [{ modifiers: ['Alt'], key: 'W' }],
            callback: () => {
                new Notice(`Write Scene`);
                this.plugin.sendNoteCommand('write_scene');
            }
        });

        this.plugin.addCommand({
            id: 'custom-prompt',
            name: 'Custom Prompt',
            hotkeys: [{ modifiers: ['Alt'], key: 'C' }],
            callback: () => {
                new Notice(`Custom Prompt`);
                this.plugin.sendNoteCommand('custom_prompt');
            }
        });

        this.plugin.addCommand({
            id: 'remove-last-response',
            name: 'Remove Last Response',
            hotkeys: [{ modifiers: ['Alt'], key: 'Z' }],
            callback: () => {
                new Notice(`Remove Last Response`);
                this.plugin.sendNoteCommand('remove_last_response');
            }
        });

        this.plugin.addCommand({
            id: 'interrupt-write',
            name: 'Interrupt Write',
            hotkeys: [{ modifiers: ['Alt'], key: 'Q' }],
            callback: () => {
                new Notice(`Interrupt Write`);
                this.plugin.sendNoteCommand('interrupt_write');
            }
        });

        this.plugin.addCommand({
            id: 'rewrite-selection',
            name: 'Rewrite selection',
            callback: () => {
                new Notice(`Rewrite selection`);
                this.plugin.rewriteSelection();
            }
        });

        this.plugin.addCommand({
            id: 'rewrite-part',
            name: 'Rewrite part',
            callback: () => {
                new Notice(`Rewrite part`);
                this.plugin.sendNoteCommand('rewrite_part');
            }
        });

        this.plugin.addCommand({
            id: 'rewrite-parts',
            name: 'Rewrite this and following parts',
            callback: () => {
                new Notice(`Rewrite this and following parts`);
                this.plugin.sendNoteCommand('rewrite_parts');
            }
        });

        this.plugin.addCommand({
            id: 'regenerate',
            name: 'Regenerate',
            callback: () => {
                new Notice(`Regenerate`);
                this.plugin.sendNoteCommand('regenerate');
            }
        });

        this.plugin.addCommand({
            id: 'add-part',
            name: 'Add Part',
            callback: () => {
                new Notice(`Add Part`);
                this.plugin.sendNoteCommand('add_part');
            }
        });

        this.plugin.addCommand({
            id: 'summarize',
            name: 'Summarize story',
            callback: () => {
                new Notice(`Summarize story`);
                this.plugin.sendNoteCommand('summarize');
            }
        });

        this.plugin.addCommand({
            id: 'update-summary',
            name: 'Update summary',
            callback: () => {
                new Notice(`Update summary`);
                this.plugin.sendNoteCommand('update_summary');
            }
        });
    }

    registerModelCommands() {
        this.plugin.addCommand({
            id: 'set-model-1',
            name: 'Set model 1',
            hotkeys: [{ modifiers: ['Alt'], key: '1' }],
            callback: async () => {
                new Notice(`Set model 1`);
                await this.plugin.setModelNumber("1");
            }
        });

        this.plugin.addCommand({
            id: 'set-model-2',
            name: 'Set model 2',
            hotkeys: [{ modifiers: ['Alt'], key: '2' }],
            callback: async () => {
                new Notice(`Set model 2`);
                await this.plugin.setModelNumber("2");
            }
        });

        this.plugin.addCommand({
            id: 'set-model-3',
            name: 'Set model 3',
            hotkeys: [{ modifiers: ['Alt'], key: '3' }],
            callback: async () => {
                new Notice(`Set model 3`);
                await this.plugin.setModelNumber("3");
            }
        });

        this.plugin.addCommand({
            id: 'set-model-4',
            name: 'Set model 4',
            hotkeys: [{ modifiers: ['Alt'], key: '4' }],
            callback: async () => {
                new Notice(`Set model 4`);
                await this.plugin.setModelNumber("4");
            }
        });

        this.plugin.addCommand({
            id: 'set-model-5',
            name: 'Set model 5',
            hotkeys: [{ modifiers: ['Alt'], key: '5' }],
            callback: async () => {
                new Notice(`Set model 5`);
                await this.plugin.setModelNumber("5");
            }
        });

        this.plugin.addCommand({
            id: 'reset-model',
            name: 'Reset model',
            hotkeys: [{ modifiers: ['Alt'], key: 'R' }],
            callback: async () => {
                new Notice(`Reset model`);
                await this.plugin.setModelNumber("");
            }
        });
    }

    registerUtilityCommands() {
        this.plugin.addCommand({
            id: 'enable-debug',
            name: 'Switch Debug Mode On/Off',
            callback: () => {
                new Notice(`Switch Debug Mode On/Off`);
                this.plugin.sendNoteCommand('switch_debug');
            }
        });
    }
}

module.exports = CommandManager;
