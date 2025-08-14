import { PluginSettingTab, Setting } from 'obsidian';
import MyPlugin from './main';

export default class MyPluginSettingTab extends PluginSettingTab {
    private plugin: MyPlugin;

    constructor(app: any, plugin: MyPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
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
