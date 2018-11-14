const https = require('https');
const fs = require('fs');

let matchesData = fs.readFileSync('./matches_data.json', {
	encoding: 'utf-8'
});

let matches = JSON.parse(matchesData);
let replaysData = {};

function downloadReplaysData() {
	let i = 0;
	let interval = setInterval(() => {
		if (i >= matches.length) {
			clearInterval(interval);
			fs.writeFileSync(`.data/replays_data/replays_data${new Date().getTime()}.json`, JSON.stringify(replaysData), 'utf-8');
		} else {
			downloadReplayData(matches[i].match_id);
			i++;
		}
	}, 1000);
}


function downloadReplayData(matchId) {
	const options = {
		hostname: 'api.opendota.com',
		path: '/api/matches/' + matchId,
	};

	https.get(options, (resp) => {
		let data = '';

		resp.on('data', (chunk) => {
			data += chunk;
		});

		resp.on('end', () => {
			let parsedData = JSON.parse(data);

			let replayData = {
				id: matchId,
				radiantWins: parsedData.radiant_win,
				duration: parsedData.duration,
				url: parsedData.replay_url
			};
			if (!parsedData.match_id) {
				console.log(matchId);
			}

			replaysData[matchId] = replayData;
			fs.writeFileSync(`./data/replays_data/replays_data${new Date().getTime()}.json`, JSON.stringify(replaysData), 'utf-8');
		});
	}).on("error", (err) => {
		console.log("Error: " + err.message);
	});
}

// downloadReplaysData();
downloadReplayData('4174654504');