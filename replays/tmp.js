const fs = require('fs');

let matchesData1 = fs.readFileSync('./replays_data1542223986448.json', {
	encoding: 'utf-8'
});

let matchesData1Obj = JSON.parse(matchesData1);
for (let i in matchesData1Obj) {
    if (!matchesData1Obj[i].url) {
        console.log(matchesData1Obj[i].id);
    }
}

console.log(Object.keys(matchesData1Obj).length);

