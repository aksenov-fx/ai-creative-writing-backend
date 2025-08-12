const { PluginSettingTab, Setting } = require('obsidian');

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

module.exports = MyPluginSettingTab;
