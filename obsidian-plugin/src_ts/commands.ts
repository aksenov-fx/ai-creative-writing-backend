import { Notice } from 'obsidian';
import { CommandConfig, CommandsHash } from './types';
import MyPlugin from './main';

export default class CommandManager {
    private plugin: MyPlugin;
    private commands: CommandsHash;

    constructor(plugin: MyPlugin) {
        this.plugin = plugin;
        this.commands = this.getCommandsHash();
    }

    private getCommandsHash(): CommandsHash {
        return {
            'set-prompt': {
                name: 'Set user prompt',
                hotkeys: [{ modifiers: ['Alt'], key: 'S' }],
                callback: () => this.plugin.communicationManager.sendNoteCommand('set_prompt')
            },
            'write-scene-or-chat': {
                name: 'Write Scene/Chat',
                hotkeys: [{ modifiers: ['Alt'], key: 'W' }],
                callback: () => this.plugin.communicationManager.sendNoteCommand('write_scene_or_chat')
            },
            'custom-prompt': {
                name: 'Custom Prompt',
                hotkeys: [{ modifiers: ['Alt'], key: 'C' }],
                callback: () => this.plugin.communicationManager.sendNoteCommand('custom_prompt')
            },
            'remove-last-response': {
                name: 'Remove Last Response',
                hotkeys: [{ modifiers: ['Alt'], key: 'Z' }],
                callback: () => this.plugin.communicationManager.sendNoteCommand('remove_last_response')
            },
            'rewrite-part': {
                name: 'Rewrite part',
                callback: () => this.plugin.communicationManager.sendNoteCommand('rewrite_part')
            },
            'rewrite-parts': {
                name: 'Rewrite this and following parts',
                callback: () => this.plugin.communicationManager.sendNoteCommand('rewrite_parts')
            },
            'regenerate': {
                name: 'Regenerate',
                callback: () => this.plugin.communicationManager.sendNoteCommand('regenerate')
            },
            'add-part': {
                name: 'Add Part',
                callback: () => this.plugin.communicationManager.sendNoteCommand('add_part')
            },
            'summarize': {
                name: 'Summarize story',
                callback: () => this.plugin.communicationManager.sendNoteCommand('summarize')
            },
            'update-summary': {
                name: 'Update summary',
                callback: () => this.plugin.communicationManager.sendNoteCommand('update_summary')
            },
            'set-model-1': {
                name: 'Set model 1',
                hotkeys: [{ modifiers: ['Alt'], key: '1' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("1")
            },
            'set-model-2': {
                name: 'Set model 2',
                hotkeys: [{ modifiers: ['Alt'], key: '2' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("2")
            },
            'set-model-3': {
                name: 'Set model 3',
                hotkeys: [{ modifiers: ['Alt'], key: '3' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("3")
            },
            'set-model-4': {
                name: 'Set model 4',
                hotkeys: [{ modifiers: ['Alt'], key: '4' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("4")
            },
            'set-model-5': {
                name: 'Set model 5',
                hotkeys: [{ modifiers: ['Alt'], key: '5' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("5")
            },
            'reset-model': {
                name: 'Reset model',
                hotkeys: [{ modifiers: ['Alt'], key: 'R' }],
                callback: async () => await this.plugin.utilityManager.setModelNumber("")
            },
            'rewrite-selection': {
                name: 'Rewrite selection',
                callback: () => this.plugin.helperManager.rewriteSelection()
            },
            'translate': {
                name: 'Translate selection',
                callback: () => this.plugin.helperManager.translateSelection()
            },
            'explain': {
                name: 'Explain selected word',
                callback: () => this.plugin.helperManager.explainWord()
            },
            'switch-debug': {
                name: 'Switch Debug Mode On/Off',
                callback: () => this.plugin.communicationManager.sendNoteCommand('switch_debug')
            },
            'interrupt-write': {
                name: 'Interrupt Write',
                hotkeys: [{ modifiers: ['Alt'], key: 'Q' }],
                callback: () => this.plugin.communicationManager.sendNoteCommand('interrupt_write')
            }
        };
    }

    registerAllCommands(): void {
        Object.entries(this.commands).forEach(([id, config]) => {
            this.registerCommand(id, config);
        });
    }

    private registerCommand(id: string, config: CommandConfig): void {
        const commandConfig: any = {
            id,
            name: config.name,
            callback: () => {
                new Notice(config.name);
                config.callback();
            }
        };

        if (config.hotkeys) {
            commandConfig.hotkeys = config.hotkeys;
        }

        this.plugin.addCommand(commandConfig);
    }
}
