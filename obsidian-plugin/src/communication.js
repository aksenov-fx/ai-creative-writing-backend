const net = require('net');

class CommunicationManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    async sendNoteCommand(methodName, selected_text = "") {
        this.plugin.app.commands.executeCommandById('editor:save-file');

        var [absoluteFolderPath, absoluteFilePath] = this.plugin.utilityManager.getPaths();
        var partNumber = this.plugin.utilityManager.getPartNumber();
        var chatMode = await this.plugin.utilityManager.getMode();

        if (methodName == "write_scene_or_chat") {
            if (chatMode) {
                methodName = "chat"
            } else {
                methodName = "write_scene"
            }
        }

        if (methodName == "remove_last_response") {
            if (chatMode) {
                methodName = "chat_remove_last_response"
            } else {
                methodName = "story_remove_last_response"
            }
        }

        var parameters = `${absoluteFolderPath},${absoluteFilePath},${methodName},${chatMode},${partNumber},${selected_text}`;

        const response = await this.sendCommandToServer(parameters);
        return response;
    }

    async sendCommandToServer(command) {
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

module.exports = CommunicationManager;