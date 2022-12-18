/*jshint esversion: 6 */

const wordOfDay = word;
var counter = 0;
var openBoxes = "";
var flagged = "";

function setCookie(item, value) {
    const d = new Date();
    var endOfDay = new Date(
        d.getFullYear(),
        d.getMonth(),
        d.getDate(),
        23,
        59,
        59
    );
    let expires = "expires=" + endOfDay.toUTCString();
    document.cookie = item + "=" + value + ";" + expires + ";";
}

function getCookie(item) {
    let name = item + "=";
    let ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

let cGuessCount = getCookie("guesses");

if (cGuessCount != "") {
    counter = parseInt(cGuessCount);
}

let cFlags = getCookie("flagged");

if (cFlags != "") {
    flagged = cFlags;
}

let cOpenBoxes = getCookie("opened");

if (cOpenBoxes != "") {
    openBoxes = cOpenBoxes;
}

document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".wrapper");
    const topWrap = document.querySelector(".topWrap");
    const wrapper2 = document.querySelector(".wrapper2");
    document.getElementById("count").innerHTML = "Guesses: " + counter;

    var alphabet = "abcdefghijklmnopqrstuvwyz".split(""); //got rid of x lol

    function createTop() {
        for (let i = 0; i < 25; i++) {
            const top = document.createElement("div");
            top.setAttribute("class", "top");
            top.setAttribute("id", alphabet[i]);
            topWrap.appendChild(top);
            top.innerHTML = alphabet[i];
        }
    }

    createTop();
    shuffle(alphabet);

    function createBoxes() {
        //adds divs with class box and id of i to wrapper div
        for (let i = 0; i < 25; i++) {
            const box = document.createElement("div");
            box.setAttribute("class", "box");
            box.setAttribute("id", i);
            wrapper.appendChild(box);

            //click function on every addition child div
            box.addEventListener("click", function() {
                testLetter(box);
                box.classList.add("invalid")
            });
            box.addEventListener("contextmenu", function(a) {
                //right click
                a.preventDefault(); //prevent context menu from popping up
                addFlag(box);
            });

        }
    }

    function animationListener() {
        wrapper2.addEventListener("animationend", function() {
            wrapper2.classList.remove("submitGlowRight");
            wrapper2.classList.remove("submitGlowWrong");
        });
    }
    animationListener();

    var bombLocs = new Array(25).fill(0); //empty array with 0s;
    setBombs(bombLocs); //function to set bomb locations as 1
    createBoxes();

    function loadGameState() {
        var openBoxesArray = openBoxes.slice(0, -1).split(",");
        var flagArray = flagged.split(",");

        for (let i = 0; i < 25; i++) {
            if (openBoxesArray.includes(i.toString())) {
                // a gamestate is saved
                var openedBoxes = document.getElementById(i);

                let index = openedBoxes.id;
                let near = bombsNearby(index);

                let target = document.getElementById(alphabet[index]);
                openedBoxes.classList.add("invalid")
                openedBoxes.innerHTML = alphabet[index] + "<sup> " + near;
                if (bombLocs[index] == 1) {
                    openedBoxes.style.backgroundColor = "#e87e72";
                    target.style.backgroundColor = "#099c13";
                    target.style.color = "#e9f0e9";

                } else {
                    if (near == 0) {
                        openedBoxes.style.backgroundColor = "#4163b9";
                    } else {
                        openedBoxes.style.backgroundColor = "#3fa0d1";
                    }
                    target.style.backgroundColor = "#a8141c";
                    target.style.textDecoration = "line-through";
                }
            } else if (flagArray.includes(i.toString())) {
                console.log(i);
                var flaggedBox = document.getElementById(i);
                flaggedBox.innerHTML = "🚩";
            }
        }
    }

    loadGameState();

    function addFlag(box) {
        if (box.innerHTML === "") box.innerHTML = "🚩";
        else if (box.innerHTML === "🚩") box.innerHTML = "";

        var flagArray = [];
        if (flagged != "") flagArray = flagged.split(",");

        console.log(flagged);
        if (flagArray.includes(box.id.toString())) {
            flagArray.splice(flagArray.indexOf(box.id));
        } else {
            flagArray.push(box.id);
        }
        flagged = flagArray.toString();
        setCookie("flagged", flagged);
    }

    function testLetter(elmo) {
        let index = elmo.id;
        let near = bombsNearby(index);
        let target = document.getElementById(alphabet[index]);
        elmo.innerHTML = alphabet[index] + " " + near;
        openBoxes = openBoxes + index + ",";
        setCookie("opened", openBoxes);

        elmo.innerHTML = alphabet[index] + "<sup> " + near;

        if (bombLocs[index] == 1) {
            elmo.style.backgroundColor = "#e87e72";
            counterAdd();
            target.style.backgroundColor = "#099c13";
            target.style.color = "#e9f0e9";
        } else {
            elmo.style.backgroundColor = "#3fa0d1";
            if (near == 0) {
                elmo.style.backgroundColor = "#4163b9";
            }
            target.style.backgroundColor = "#a8141c";
            target.style.textDecoration = "line-through";
        }
    }

    function setBombs(arr) {
        for (let i = 0; i < 25; i++) {
            if (wordOfDay.includes(alphabet[i])) {
                arr[i] = 1;
            }
        }
    }

    //list of cases far left, far right, top, and bottom
    function bombsNearby(index) {
        let i = Number(index);
        let total = 0;
        const farLeft = i < 5;
        const farRight = i > 19;
        const top = i % 5 === 0;
        const bottom = i % 5 === 4;

        if (!farLeft) {
            if (!top && bombLocs[i - 6] === 1) total++;
            if (bombLocs[i - 5] === 1) total++;
            if (!bottom && bombLocs[i - 4] === 1) total++;
        }

        if (!farRight) {
            if (!top && bombLocs[i + 4] === 1) total++;
            if (bombLocs[i + 5] === 1) total++;
            if (!bottom && bombLocs[i + 6] === 1) total++;
        }
        if (!top) {
            if (bombLocs[i - 1] === 1) total++;
        }
        if (!bottom) {
            if (bombLocs[i + 1] === 1) total++;
        }

        return total;
    }

    function shuffle(array) {
        var generator = new Math.seedrandom(seed);
        //random shuffling array found online
        for (var i = array.length - 1; i > 0; i--) {
            var j = Math.floor(generator() * (i + 1));
            var temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }

    function onEnter() {
        const input = document.querySelector("#ansInput")
        input.addEventListener("keypress", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                document.getElementById("button-addon2").click();
            };
        });
    }
    onEnter()
});

function getData() {
    let myInput = document.getElementById("ansInput").value.toLowerCase();
    let submitWrapper = document.querySelector(".wrapper2");
    if (myInput === wordOfDay) {
        submitWrapper.classList.add("submitGlowRight");
        counterAdd();
        const request = new XMLHttpRequest();
        request.open("POST", `/submit/${JSON.stringify(counter)}`);
        request.send();
        $("#submit-modal").modal("show");
        document.querySelector(".wrapper2 button").style.pointerEvents = "none";
        document.querySelector(".wrapper2 input").style.pointerEvents = "none";
        document.querySelector(".wrapper2").style.cursor = "not-allowed";
    } else {
        counterAdd();
        submitWrapper.classList.add("submitGlowWrong");
    }
    document.getElementById("ansInput").value = "";
}

function counterAdd() {
    counter++;
    document.getElementById("count").innerHTML = "Guesses: " + counter;
    setCookie("guesses", counter);
}

function getPastData() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var raw_data = JSON.parse(request.responseText);
            console.log(raw_data);
            var current_date = new Date();
            var old_date = new Date();
            if (raw_data[0] === null) {
                document.querySelector("#mean_guesses").textContent =
                    "Mean Guesses (7 days): Undefined";
                document.querySelector("#rank_score").textContent =
                    "Average Score (7 days): Undefined";
                document.querySelector("#no_of_attempts").textContent =
                    "Attempts (7 days): 0";
            } else {
                document.querySelector(
                    "#mean_guesses"
                ).textContent = `Mean Guesses (7 days): ${raw_data[4]}`;
                document.querySelector(
                    "#rank_score"
                ).textContent = `Average Score (7 days): ${raw_data[5]}`;
                document.querySelector(
                    "#no_of_attempts"
                ).textContent = `Attempts (7 days): ${raw_data[6]}`;
            }
            old_date.setDate(old_date.getDate() - 7);
            let chartStatus = Chart.getChart("myChart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.destroy();
            }
            let chartStatus2 = Chart.getChart("myChart2"); // <canvas> id
            if (chartStatus2 != undefined) {
                chartStatus2.destroy();
            }
            console.log(raw_data);
            // ** SETUP
            const data = {
                datasets: [{
                    label: "Your Score",
                    backgroundColor: "rgb(17,78,111)",
                    borderColor: "rgb(17,78,111)",
                    data: raw_data[7],
                }, ],
            };
            // ** SETUP
            const config = {
                type: "line",
                data: data,
                options: {
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "day",
                                tooltipFormat: "yyyy-MM-dd",
                            },
                            min: old_date,
                            max: current_date,
                        },
                        y: {
                            max: 100,
                            beginAtZero: 1,
                            ticks: {
                                stepSize: 10,
                            },
                        },
                    },
                },
            };
            // ** SETUP
            const ctx = document.getElementById("myChart").getContext("2d");

            myChart = new Chart(ctx, config);

            // ** SETUP
            const data2 = {
                datasets: [{
                        label: "Your Score",
                        backgroundColor: "rgb(17,78,111)",
                        borderColor: "rgb(17,78,111)",
                        data: raw_data[0],
                    },
                    {
                        label: "top 90%",
                        borderColor: "rgb(255, 97, 80)",
                        data: raw_data[1],
                        borderDash: [10, 5],
                    },
                    {
                        label: "top 50%",
                        borderColor: "rgb(26, 192, 198)",
                        data: raw_data[2],
                        borderDash: [10, 5],
                    },
                    {
                        label: "top 10%",
                        borderColor: "rgb(88, 179, 104)",
                        data: raw_data[3],
                        borderDash: [10, 5],
                    },
                ],
            };
            // ** SETUP
            const config2 = {
                type: "line",
                data: data2,
                options: {
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "day",
                                tooltipFormat: "yyyy-MM-dd",
                            },
                            min: old_date,
                            max: current_date,
                        },
                        y: {
                            max: 10,
                            beginAtZero: 1,
                            ticks: {
                                stepSize: 1,
                            },
                        },
                    },
                },
            };
            // ** SETUP
            const ctx2 = document.getElementById("myChart2").getContext("2d");

            myChart2 = new Chart(ctx2, config2);
        }
    };
    request.open("GET", "/result");
    request.send();
}