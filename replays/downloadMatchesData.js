const https = require('https');
const fs = require('fs');

let replaysData = [];

let getReplays = function (lessThanMatchId) {
	const options = {
		hostname: 'api.opendota.com',
		path: '/api/proMatches?less_than_match_id=' + lessThanMatchId,
	};

	https.get(options, (resp) => {
		let data = '';

		resp.on('data', (chunk) => {
			data += chunk;
		});

		resp.on('end', () => {
			let parsedData = JSON.parse(data);
			replaysData.push(...parsedData);
			lessThanMatchId = parsedData.slice(-1)[0].match_id;
			if (replaysData.length < 1000) {
				getReplays(lessThanMatchId);
			} else {
				fs.writeFileSync('./matches_data.json', JSON.stringify(replaysData), 'utf-8');
				console.log(replaysData.length);
			}
		});

	}).on("error", (err) => {
		console.log("Error: " + err.message);
	});
};

getReplays('');