const http = require('http');
const fs = require('fs');

let replaysData = fs.readFileSync('./data/replays_data/replays_data.json');
let parsedReplaysData = JSON.parse(replaysData);
let replaysDataArr = [];

for (let key in parsedReplaysData) {
    replaysDataArr.push(parsedReplaysData[key]);
}

function downloadReplay(url) {
    let fileName = url.substring(url.lastIndexOf('/'));
    let filePath = 'H:/Minchuk/replays' + fileName;

    return new Promise((resolve, reject) => {
        if (!fs.existsSync(filePath)) {
            let file = fs.createWriteStream(filePath);

            http.get(url, { timeout: 120 * 1000 }, (resp) => {
                console.log(resp.statusCode);
                console.log(resp.statusMessage);

                if (resp.statusCode !== 200) {
                    reject(resp.statusCode);
                }

                resp.on('aborted', () => {
                    if (!resp.complete) {
                        console.error('The connection was aborted while the message was still being sent');
                        console.log(`aborted ${url}`);
                        reject();
                    }
                });

                if (resp.isPaused()) {
                    console.log('paused');
                    resp.resume();
                }

                resp.pipe(file);

                resp.on('error', (e) => {
                    reject(e);
                });

                resp.on('end', () => {
                    if (!resp.complete) {
                        console.error('The connection was terminated while the message was still being sent');
                        reject();
                    } else {
                        resolve();
                    }
                });
            }).on('error', (err) => {
                reject('Error: ' + err.message);
            });
        } else {
            reject('File already exists: ' + fileName);
        }
    });
}

async function downloadReplays(start, end) {
    start = start || 0;
    end = end || replaysDataArr.length;

    for (let i = start; i < end; i++) {
        let attempts = 3;

        while (attempts) {
            try {
                await downloadReplay(replaysDataArr[i].url);
                attempts = 0;
            } catch (e) {
                console.error(e);
                attempts--;
            }
        }
    }
}

downloadReplays(960);