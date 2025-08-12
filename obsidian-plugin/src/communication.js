const net = require('net');

class CommunicationManager {
    constructor(plugin) {
        this.plugin = plugin;
    }

    async sendNoteCommand(methodName, selected_text = "") {
        this.plugin.app.commands.executeCommandById('editor:save-file');

        var absoluteFolderPath = this.plugin.getNotePath();
        var partNumber = this.plugin.getPartNumber();
        var parameters = `${absoluteFolderPath},${methodName},${partNumber},${selected_text}`;

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