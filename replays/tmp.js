const fs = require('fs');

let matchesData1 = fs.readFileSync('./data/replays_data/replays_data.json', {
    encoding: 'utf-8'
});

let max = 0;
let maxUrl = '';
let matchesData1Obj = JSON.parse(matchesData1);
let matchesDataArr = [];

for (let i in matchesData1Obj) {
    matchesDataArr.push(matchesData1Obj[i]);
}


matchesDataArr.forEach((match, i) => {
    // let durMin = match.duration / 60;
    // if (durMin < 15) {
    //     console.log(matchesData1Obj[i].id);
    //     console.log(durMin);
    // }
    // if (durMin > max) {
    //     max = durMin;
    //     maxUrl = matchesData1Obj[i].id;
    // }
    if (match.id === 4208237598) {
        console.log(i);
    }
});

// console.log(max);
// console.log(maxUrl);