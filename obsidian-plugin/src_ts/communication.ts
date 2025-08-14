import * as net from 'net';
import MyPlugin from './main';

export default class CommunicationManager {
    private plugin: MyPlugin;

    constructor(plugin: MyPlugin) {
        this.plugin = plugin;
    }

    async sendNoteCommand(methodName: string, selected_text: string = ""): Promise<string> {
        // @ts-ignore - Obsidian API limitation
        this.plugin.app.commands.executeCommandById('editor:save-file');

        const [absoluteFolderPath, absoluteFilePath] = this.plugin.utilityManager.getPaths();
        const partNumber = this.plugin.utilityManager.getPartNumber();
        const chatMode = await this.plugin.utilityManager.getMode();

        let finalMethodName = methodName;
        if (methodName === "write_scene_or_chat") {
            if (chatMode) {
                finalMethodName = "chat";
            } else {
                finalMethodName = "write_scene";
            }
        }

        if (methodName === "remove_last_response") {
            if (chatMode) {
                finalMethodName = "chat_remove_last_response";
            } else {
                finalMethodName = "story_remove_last_response";
            }
        }

        const parameters = `${absoluteFolderPath},${absoluteFilePath},${finalMethodName},${chatMode},${partNumber},${selected_text}`;

        const response = await this.sendCommandToServer(parameters);
        return response;
    }

    private async sendCommandToServer(command: string): Promise<string> {
        return new Promise((resolve, reject) => {
            const client = new net.Socket();
            let response = '';
            
            client.connect(9993, 'localhost', () => {
                console.log('Connected to Python server');
                client.write(command);
            });
    
            client.on('data', (data) => {
                response += data.toString();
                client.destroy();
            });
    
            client.on('close', () => {
                console.log('Connection closed');
                resolve(response);
            });
    
            client.on('error', (err) => {
                console.error('Connection error: ', err);
                reject(err);
            });
        });
    }
}
