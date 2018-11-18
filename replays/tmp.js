const fs = require('fs');

let matchesData1 = fs.readFileSync('./data/replays_data/replays_data.json', {
    encoding: 'utf-8'
});

let matchesData1Obj = JSON.parse(matchesData1);
let matchesDataArr = [];

for (let i in matchesData1Obj) {
    matchesDataArr.push(matchesData1Obj[i]);
}

let duration = 0;
matchesDataArr.forEach((match, i) => {
    let durMin = match.duration / 60;
    duration += durMin;
});

matchesDataArr.sort((a, b) => {
    if (a.duration > b.duration) {
        return 1;
    } else if (a.duration < b.duration) {
        return -1;
    } else {
        return 0;
    }
});

console.log(matchesDataArr[matchesDataArr.length / 2].duration / 60);
console.log(duration / matchesDataArr.length);
